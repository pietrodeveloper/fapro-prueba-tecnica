# app/uf/validators.py
from datetime import date, datetime

from app.core.errors import InvalidDateError

MIN_DATE = date(2013, 1, 1)

def validate_date(date_str: str) -> date:
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidDateError("Invalid date format. Use YYYY-MM-DD")

    if parsed < MIN_DATE:
        raise InvalidDateError("Date must be >= 2013-01-01")

    if parsed > date.today():
        raise InvalidDateError("Date cannot be in the future")

    return parsed