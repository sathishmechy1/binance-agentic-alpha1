import time
import requests


class BinanceMCPServer:
    """
    Agentic Alpha Binance market-data adapter.

    Uses Binance public market-data endpoints.
    Automatically tries multiple official Binance endpoints
    if one endpoint is unavailable or returns an error.
    """

    DEFAULT_ENDPOINTS = [
        "https://data-api.binance.vision",
        "https://api-gcp.binance.com",
        "https://api1.binance.com",
        "https://api2.binance.com",
        "https://api3.binance.com",
        "https://api4.binance.com",
        "https://api.binance.com",
    ]

    def __init__(self, endpoints=None):
        self.endpoints = endpoints or self.DEFAULT_ENDPOINTS
        self.active_endpoint = None
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "AgenticAlpha/1.0",
                "Accept": "application/json",
            }
        )

    def _get(self, path, params=None):
        """
        Request Binance public market data.

        Automatically fails over to another Binance endpoint
        when an endpoint returns 403, 429, 5xx, or a connection error.
        """

        errors = []

        for base_url in self.endpoints:
            url = f"{base_url}{path}"

            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=8,
                )

                if response.status_code == 200:
                    self.active_endpoint = base_url
                    return response.json()

                errors.append(
                    f"{base_url} -> HTTP {response.status_code}"
                )

            except requests.RequestException as error:
                errors.append(
                    f"{base_url} -> {type(error).__name__}"
                )

            # Small delay before trying another endpoint
            time.sleep(0.15)

        raise RuntimeError(
            "Binance market-data endpoints failed:\n"
            + "\n".join(errors)
        )

    def get_market_data(self, symbol):
        """
        Get 24h ticker and order-book data.
        """

        symbol = symbol.upper().strip()

        ticker = self._get(
            "/api/v3/ticker/24hr",
            {
                "symbol": symbol
            }
        )

        depth = self._get(
            "/api/v3/depth",
            {
                "symbol": symbol,
                "limit": 20
            }
        )

        return {
            "symbol": symbol,
            "price": float(ticker["lastPrice"]),
            "change_percent": float(
                ticker["priceChangePercent"]
            ),
            "volume": float(
                ticker["quoteVolume"]
            ),
            "high": float(
                ticker["highPrice"]
            ),
            "low": float(
                ticker["lowPrice"]
            ),
            "bids": depth["bids"],
            "asks": depth["asks"],
            "endpoint": self.active_endpoint,
        }

    def get_klines(
        self,
        symbol,
        interval="5m",
        limit=100
    ):
        """
        Get candlestick data.
        """

        return self._get(
            "/api/v3/klines",
            {
                "symbol": symbol.upper().strip(),
                "interval": interval,
                "limit": limit,
            }
        )

    def get_order_book(
        self,
        symbol,
        limit=20
    ):
        """
        Get order-book depth.
        """

        return self._get(
            "/api/v3/depth",
            {
                "symbol": symbol.upper().strip(),
                "limit": limit,
            }
        )

    def execute_market_order(
        self,
        symbol,
        side,
        quantity
    ):
        """
        Trading is intentionally disabled in this version.
        """

        raise RuntimeError(
            "Order execution is not enabled."
        )


if __name__ == "__main__":
    client = BinanceMCPServer()

    data = client.get_market_data("BTCUSDT")

    print("Agentic Alpha Binance Adapter")
    print(f"Symbol: {data['symbol']}")
    print(f"Price: ${data['price']:,.2f}")
    print(
        f"24h Change: "
        f"{data['change_percent']:+.2f}%"
    )
    print(
        f"Endpoint: "
        f"{data['endpoint']}"
    )
