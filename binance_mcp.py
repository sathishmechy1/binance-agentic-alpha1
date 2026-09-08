import requests

class BinanceMCPServer:
    """Read-only Binance public market-data adapter."""

    def __init__(self, base_url="https://api.binance.com"):
        self.base_url = base_url.rstrip("/")

    def _get(self, path, params=None):
        r = requests.get(f"{self.base_url}{path}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get_market_data(self, symbol: str):
        symbol = symbol.upper()
        ticker = self._get("/api/v3/ticker/24hr", {"symbol": symbol})
        depth = self._get("/api/v3/depth", {"symbol": symbol, "limit": 20})
        return {
            "symbol": symbol,
            "price": float(ticker["lastPrice"]),
            "change_percent": float(ticker["priceChangePercent"]),
            "volume": float(ticker["quoteVolume"]),
            "high": float(ticker["highPrice"]),
            "low": float(ticker["lowPrice"]),
            "bids": depth["bids"],
            "asks": depth["asks"],
        }

    def get_klines(self, symbol: str, interval="5m", limit=50):
        rows = self._get("/api/v3/klines", {
            "symbol": symbol.upper(), "interval": interval, "limit": limit
        })
        return rows

    def execute_market_order(self, *args, **kwargs):
        raise RuntimeError(
            "Execution is disabled in this version. This project is read-only/paper-trading."
        )
