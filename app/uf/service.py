from __future__ import annotations

from dataclasses import asdict

from app.uf.scraper import fetch_uf_from_sii
from app.uf.validators import validate_date

def get_uf_value(date: str) -> dict:
    """
    Returns:
        {"date": "...", "value": "..."}  (JSON-serializable dict)

    Raises:
        ValueError: invalid date (from validate_date)
        UFNotFoundError: UF not found for that date
        UFSourceError: issues contacting SII
    """
    validate_date(date)

    result = fetch_uf_from_sii(date)
    return asdict(result)