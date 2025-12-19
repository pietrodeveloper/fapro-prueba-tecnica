from __future__ import annotations

from dataclasses import asdict

from app.uf.scraper import fetch_uf_from_sii
from app.uf.validators import validate_date

"""UF service.

Provides `get_uf_value(date: str) -> dict` which validates the input date
and returns the UF value fetched from SII as a JSON-serializable dict.

Raises domain errors from lower layers: `InvalidDateError`, `UFNotFoundError`,
and `UFSourceError`.
"""

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