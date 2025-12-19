"""Custom exceptions used by the UF service.

Defines concise, domain-specific errors raised by validation and scraping
operations when handling UF requests.

Exceptions:
- InvalidDateError: invalid format, out-of-range, or future dates.
- UFNotFoundError: UF value not found for a valid date.
- UFSourceError: problems contacting or parsing the SII source.
"""


class InvalidDateError(ValueError):
    """Invalid or out-of-range date."""
    pass


class UFNotFoundError(LookupError):
    """UF value not found for the requested date."""
    pass


class UFSourceError(RuntimeError):
    """Problems contacting or reading the SII source."""
    pass