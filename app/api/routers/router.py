from fastapi import APIRouter, HTTPException, status

from app.uf.scraper import UFNotFoundError, UFSourceError
from app.uf.service import get_uf_value

router = APIRouter(prefix="/uf", tags=["uf"])

"""UF API router.

Defines the `/uf/{date}` endpoint that returns the UF value for a given
date (YYYY-MM-DD). Domain errors are translated to proper HTTP responses.
"""
@router.get("/{date}")
def read_uf(date: str):
    """
    date format: YYYY-MM-DD
    """
    try:
        return get_uf_value(date)
    except ValueError as e:
        # inválido: formato o fuera de rango
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e) or "Invalid date",
        ) from e
    except UFNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UF value not found for the given date",
        ) from e
    except UFSourceError as e:
        # problemas con SII (caído, html cambió, timeout, etc.)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error fetching UF value from source",
        ) from e