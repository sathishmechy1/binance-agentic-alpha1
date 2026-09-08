import os

class RiskManager:
    def __init__(self):
        self.max_trade_size = float(os.getenv("MAX_TRADE_SIZE_USDT", "100"))
        self.max_drawdown = float(os.getenv("MAX_DRAWDOWN_PERCENT", "2.0"))

    def validate_trade(self, price: float, quantity: float, signal: str):
        trade_value = price * quantity
        if trade_value > self.max_trade_size:
            return False, f"Size ${trade_value:.2f} exceeds ${self.max_trade_size:.2f} limit."
        if signal not in {"BUY", "SELL"}:
            return False, "No executable signal."
        return True, "Risk check passed (paper mode)."
