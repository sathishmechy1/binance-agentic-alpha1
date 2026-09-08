import requests


class BinanceMCPServer:

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

    def _get(self, path, params=None):

        errors = []

        for base_url in self.endpoints:

            try:

                response = requests.get(
                    f"{base_url}{path}",
                    params=params,
                    timeout=10,
                    headers={
                        "User-Agent": "AgenticAlpha/1.0"
                    },
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

        raise RuntimeError(
            "Binance market-data endpoints failed:\n"
            + "\n".join(errors)
        )

    def get_market_data(self, symbol):

        symbol = symbol.upper()

        ticker = self._get(
            "/api/v3/ticker/24hr",
            {"symbol": symbol}
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
            "endpoint": self.active_endpoint
        }

    def get_klines(
        self,
        symbol,
        interval="5m",
        limit=100
    ):

        return self._get(
            "/api/v3/klines",
            {
                "symbol": symbol.upper(),
                "interval": interval,
                "limit": limit
            }
        )

    def get_order_book(
        self,
        symbol,
        limit=20
    ):

        data = self._get(
            "/api/v3/depth",
            {
                "symbol": symbol.upper(),
                "limit": limit
            }
        )

        return data

    def execute_market_order(
        self,
        symbol,
        side,
        quantity
    ):

        raise RuntimeError(
            "Order execution is not enabled."
        )


if __name__ == "__main__":

    client = BinanceMCPServer()

    data = client.get_market_data(
        "BTCUSDT"
    )

    print("Agentic Alpha Binance Adapter")
    print(
        f"Symbol: {data['symbol']}"
    )
    print(
        f"Price: ${data['price']:,.2f}"
    )
    print(
        f"24h Change: "
        f"{data['change_percent']:+.2f}%"
        )
