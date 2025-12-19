import pytest

from app.core.errors import UFNotFoundError, UFSourceError
from app.uf.scraper import fetch_uf_from_sii


class DummyResponse:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text


def test_fetch_uf_non_200_raises_source_error(monkeypatch):
    def fake_get(url, timeout):
        return DummyResponse(500, "error")

    monkeypatch.setattr("app.uf.scraper.requests.get", fake_get)

    with pytest.raises(UFSourceError):
        fetch_uf_from_sii("2024-01-10")


def test_fetch_uf_not_found_raises(monkeypatch):
    # HTML válido pero sin el div/tabla esperados -> parse devuelve None -> UFNotFoundError
    html = "<html><body><div id='mes_enero'><table></table></div></body></html>"

    def fake_get(url, timeout):
        return DummyResponse(200, html)

    monkeypatch.setattr("app.uf.scraper.requests.get", fake_get)

    with pytest.raises(UFNotFoundError):
        fetch_uf_from_sii("2024-01-10")


def test_fetch_uf_ok(monkeypatch):
    # Estructura mínima para que _parse_uf_value encuentre:
    # div id=mes_enero, table, th "10", td siguiente "36.123,45"
    html = """
    <html><body>
      <div id="mes_enero">
        <table>
          <tr><th>10</th><td>36.123,45</td></tr>
        </table>
      </div>
    </body></html>
    """

    def fake_get(url, timeout):
        return DummyResponse(200, html)

    monkeypatch.setattr("app.uf.scraper.requests.get", fake_get)

    result = fetch_uf_from_sii("2024-01-10")
    assert result.date == "2024-01-10"
    assert result.value == "36.123,45"