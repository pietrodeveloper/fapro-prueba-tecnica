class InvalidDateError(ValueError):
    """The provided date is invalid or out of range."""
    pass

class UFNotFoundError(LookupError):
    """UF value not found for the requested date."""
    pass

class UFSourceError(RuntimeError):
    """Problems contacting or reading the SII source."""
    pass