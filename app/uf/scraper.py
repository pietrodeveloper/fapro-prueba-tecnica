from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests
from app.core.errors import UFNotFoundError, UFSourceError
from bs4 import BeautifulSoup

"""Scraper for UF values from the Chilean SII website.

Provides `fetch_uf_from_sii(date: str) -> UFResult` which scrapes the SII
UF pages and returns the date and value as strings. Raises domain errors:
`UFSourceError` for network / source issues and `UFNotFoundError` when a
valid date has no value in the page.
"""

SII_UF_URL_TEMPLATE = "https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"

@dataclass(frozen=True)
class UFResult:
    date: str
    value: str

def fetch_uf_from_sii(date: str, timeout: float = 10.0) -> UFResult:
    """
    Fetch UF value for a specific date (YYYY-MM-DD) from SII (Chile) by scraping.

    Returns:
        UFResult(date=..., value=...) where value is a string as shown in the site.

    Raises:
        UFSourceError: network / non-200 responses.
        UFNotFoundError: date exists but value isn't found in the HTML.
    """
    year, month, day = _split_date(date)
    url = SII_UF_URL_TEMPLATE.format(year=year)

    try:
        resp = requests.get(url, timeout=timeout)
    except requests.RequestException as e:
        raise UFSourceError(f"Error fetching SII UF page: {e}") from e

    if resp.status_code != 200:
        raise UFSourceError(f"SII responded with status {resp.status_code}")

    value = _parse_uf_value(resp.text, month=month, day=day)
    if value is None:
        raise UFNotFoundError(f"UF value not found for date {date}")

    return UFResult(date=date, value=value)

def _parse_uf_value(html: str, month: int, day: int) -> Optional[str]:
    """
    Parse UF value from SII HTML for a given month/day.
    Returns the value as string (e.g. '36.123,45') or None if not found.
    """
    soup = BeautifulSoup(html, "html.parser")

    # In SII UF page, months are typically sections like <div id="mes_Enero"> ... </div>
    month_name_es = _month_name_es(month)
    month_div_id = f"mes_{month_name_es}"
    
    print(f"[DEBUG] Looking for month div: {month_div_id}")

    month_div = soup.find("div", {"id": month_div_id})
    if not month_div:
        print(f"[DEBUG] Month div NOT found for {month_div_id}")
        # Let's see what divs ARE available
        all_divs = soup.find_all("div", id=True)
        print(f"[DEBUG] Available divs with id: {[d.get('id') for d in all_divs[:10]]}")
        return None

    print("[DEBUG] Month div found!")
    table = month_div.find("table")
    if not table:
        print("[DEBUG] Table NOT found in month div")
        return None

    print("[DEBUG] Table found!")
    # Rows contain day in <th> and value in next <td>
    # We look for a <th> exactly matching the day number
    day_str = str(day)
    print(f"[DEBUG] Looking for day: '{day_str}'")
    
    # Let's see what th elements exist
    all_ths = table.find_all("th")
    print(f"[DEBUG] First 10 th elements: {[th.get_text(strip=True) for th in all_ths[:10]]}")
    
    th = table.find(lambda tag: tag.name == "th" and tag.string == day_str)
    if not th:
        print(f"[DEBUG] TH NOT found for day '{day_str}'")
        return None

    print(f"[DEBUG] TH found for day '{day_str}'!")
    td = th.find_next("td")
    if not td:
        print("[DEBUG] TD NOT found after th")
        return None

    value = td.get_text(strip=True)
    print(f"[DEBUG] Value found: '{value}'")
    return value or None

def _split_date(date: str) -> tuple[int, int, int]:
    y, m, d = date.split("-")
    return int(y), int(m), int(d)

def _month_name_es(month: int) -> str:
    """
    Returns Spanish month name in lowercase, matching SII HTML ids.
    """
    # We avoid locale dependency (locale.setlocale) for portability.
    months = [
        "",  # 0 placeholder
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    if month < 1 or month > 12:
        raise ValueError("Invalid month")
    return months[month]
