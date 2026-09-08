from .risk_manager import RiskManager

class AgenticAlphaOS:
    def __init__(self, market_adapter, sentiment_adapter=None):
        self.market = market_adapter
        self.sentiment = sentiment_adapter
        self.risk = RiskManager()

    @staticmethod
    def order_book_pressure(bids, asks):
        bid_value = sum(float(p) * float(q) for p, q in bids)
        ask_value = sum(float(p) * float(q) for p, q in asks)
        total = bid_value + ask_value
        ratio = (bid_value / total) if total else 0.5
        if ratio >= 0.55:
            label = "BUY PRESSURE"
        elif ratio <= 0.45:
            label = "SELL PRESSURE"
        else:
            label = "BALANCED"
        return ratio, label

    @staticmethod
    def momentum(change_percent):
        if change_percent >= 2:
            return "STRONG BULLISH"
        if change_percent > 0.25:
            return "BULLISH"
        if change_percent <= -2:
            return "STRONG BEARISH"
        if change_percent < -0.25:
            return "BEARISH"
        return "NEUTRAL"

    def analyze(self, symbol):
        data = self.market.get_market_data(symbol)
        ratio, pressure = self.order_book_pressure(data["bids"], data["asks"])
        mom = self.momentum(data["change_percent"])

        if mom in {"STRONG BULLISH", "BULLISH"} and pressure == "BUY PRESSURE":
            signal = "BUY"
        elif mom in {"STRONG BEARISH", "BEARISH"} and pressure == "SELL PRESSURE":
            signal = "SELL"
        else:
            signal = "HOLD"

        suggested_usdt = min(50.0, self.risk.max_trade_size)
        quantity = suggested_usdt / data["price"] if data["price"] else 0
        ok, reason = self.risk.validate_trade(data["price"], quantity, signal)

        return {
            **data,
            "order_book_ratio": ratio,
            "order_pressure": pressure,
            "momentum": mom,
            "signal": signal,
            "suggested_usdt": suggested_usdt,
            "quantity": quantity,
            "risk_ok": ok,
            "risk_reason": reason,
        }
