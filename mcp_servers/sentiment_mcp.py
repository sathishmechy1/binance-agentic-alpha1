class SentimentMCPServer:
    """Placeholder sentiment adapter. No fake random score is used."""

    def get_sentiment_score(self, symbol: str) -> dict:
        return {
            "symbol": symbol.upper(),
            "sentiment_score": 0.0,
            "signal": "UNAVAILABLE",
            "source": "Not connected"
        }
