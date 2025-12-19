from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests
from app.core.errors import UFNotFoundError, UFSourceError
from bs4 import BeautifulSoup

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

    month_div = soup.find("div", {"id": month_div_id})
    if not month_div:
        return None

    table = month_div.find("table")
    if not table:
        return None

    # Rows contain day in <th> and value in next <td>
    # We look for a <th> exactly matching the day number
    day_str = str(day)
    th = table.find("th", string=day_str)
    if not th:
        return None

    td = th.find_next("td")
    if not td:
        return None

    value = td.get_text(strip=True)
    return value or None

def _split_date(date: str) -> tuple[int, int, int]:
    y, m, d = date.split("-")
    return int(y), int(m), int(d)

def _month_name_es(month: int) -> str:
    """
    Returns Spanish month name with first letter capitalized, matching SII HTML ids.
    """
    # We avoid locale dependency (locale.setlocale) for portability.
    months = [
        "",  # 0 placeholder
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    ]
    if month < 1 or month > 12:
        raise ValueError("Invalid month")
    return months[month]
