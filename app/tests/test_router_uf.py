from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routers.router import router
from app.core.errors import UFNotFoundError, UFSourceError


def make_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_uf_ok(monkeypatch):
    client = make_client()

    def fake_get_uf_value(date: str):
        return {"date": date, "value": "36000,00"}

    monkeypatch.setattr("app.api.routers.router.get_uf_value", fake_get_uf_value)

    r = client.get("/uf/2024-01-10")
    assert r.status_code == 200
    assert r.json() == {"date": "2024-01-10", "value": "36000,00"}


def test_uf_invalid_date_returns_400(monkeypatch):
    client = make_client()

    def fake_get_uf_value(date: str):
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    monkeypatch.setattr("app.api.routers.router.get_uf_value", fake_get_uf_value)

    r = client.get("/uf/10-01-2024")
    assert r.status_code == 400
    assert "Invalid date format" in r.json()["detail"]


def test_uf_not_found_returns_404(monkeypatch):
    client = make_client()

    def fake_get_uf_value(date: str):
        raise UFNotFoundError("UF value not found")

    monkeypatch.setattr("app.api.routers.router.get_uf_value", fake_get_uf_value)

    r = client.get("/uf/2024-01-10")
    assert r.status_code == 404
    assert r.json()["detail"] == "UF value not found for the given date"


def test_uf_source_error_returns_502(monkeypatch):
    client = make_client()

    def fake_get_uf_value(date: str):
        raise UFSourceError("SII down")

    monkeypatch.setattr("app.api.routers.router.get_uf_value", fake_get_uf_value)

    r = client.get("/uf/2024-01-10")
    assert r.status_code == 502
    assert r.json()["detail"] == "Error fetching UF value from source"