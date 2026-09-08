class AgenticAlphaOS:

    def __init__(self, market_adapter):
        self.market = market_adapter

    # -----------------------------
    # ORDER BOOK ANALYSIS
    # -----------------------------

    @staticmethod
    def order_book_analysis(bids, asks):

        bid_value = sum(
            float(price) * float(quantity)
            for price, quantity in bids
        )

        ask_value = sum(
            float(price) * float(quantity)
            for price, quantity in asks
        )

        total = bid_value + ask_value

        if total <= 0:
            return {
                "bid_share": 0.5,
                "imbalance": 0.0,
                "pressure": "BALANCED"
            }

        bid_share = bid_value / total

        imbalance = (
            (bid_value - ask_value) / total
        )

        if bid_share >= 0.55:
            pressure = "BUY PRESSURE"

        elif bid_share <= 0.45:
            pressure = "SELL PRESSURE"

        else:
            pressure = "BALANCED"

        return {
            "bid_share": bid_share,
            "imbalance": imbalance,
            "pressure": pressure
        }

    # -----------------------------
    # MOMENTUM
    # -----------------------------

    @staticmethod
    def momentum_analysis(change):

        if change >= 3:
            return "STRONG BULLISH", 90

        if change >= 1:
            return "BULLISH", 75

        if change > 0.25:
            return "MILD BULLISH", 60

        if change <= -3:
            return "STRONG BEARISH", 10

        if change <= -1:
            return "BEARISH", 25

        if change < -0.25:
            return "MILD BEARISH", 40

        return "NEUTRAL", 50

    # -----------------------------
    # VOLUME ANALYSIS
    # -----------------------------

    @staticmethod
    def volume_analysis(volume):

        if volume >= 1_000_000_000:
            return "VERY HIGH"

        if volume >= 500_000_000:
            return "HIGH"

        if volume >= 100_000_000:
            return "NORMAL"

        return "LOW"

    # -----------------------------
    # MARKET REGIME
    # -----------------------------

    @staticmethod
    def market_regime(momentum, pressure):

        bullish = {
            "BULLISH",
            "STRONG BULLISH",
            "MILD BULLISH"
        }

        bearish = {
            "BEARISH",
            "STRONG BEARISH",
            "MILD BEARISH"
        }

        if momentum in bullish and pressure == "BUY PRESSURE":
            return "BULLISH TREND"

        if momentum in bearish and pressure == "SELL PRESSURE":
            return "BEARISH TREND"

        if momentum == "NEUTRAL":
            return "RANGING / NEUTRAL"

        return "MIXED / TRANSITION"

    # -----------------------------
    # AGENT DECISION
    # -----------------------------

    @staticmethod
    def decision(momentum, pressure, confidence):

        bullish = {
            "BULLISH",
            "STRONG BULLISH"
        }

        bearish = {
            "BEARISH",
            "STRONG BEARISH"
        }

        if (
            momentum in bullish
            and pressure == "BUY PRESSURE"
            and confidence >= 65
        ):
            return "BUY"

        if (
            momentum in bearish
            and pressure == "SELL PRESSURE"
            and confidence >= 65
        ):
            return "SELL"

        return "HOLD"

    # -----------------------------
    # COMPLETE ANALYSIS
    # -----------------------------

    def analyze(self, symbol):

        market = self.market.get_market_data(symbol)

        price = market["price"]
        change = market["change_percent"]
        volume = market["volume"]

        # Order book
        book = self.order_book_analysis(
            market["bids"],
            market["asks"]
        )

        # Momentum
        momentum, momentum_score = (
            self.momentum_analysis(change)
        )

        # Volume
        volume_activity = self.volume_analysis(
            volume
        )

        # Market regime
        regime = self.market_regime(
            momentum,
            book["pressure"]
        )

        # -------------------------
        # CONFIDENCE MODEL
        # -------------------------

        confidence = 50

        if book["pressure"] == "BUY PRESSURE":
            confidence += 20

        elif book["pressure"] == "SELL PRESSURE":
            confidence += 20

        if momentum in {
            "STRONG BULLISH",
            "STRONG BEARISH"
        }:
            confidence += 20

        elif momentum in {
            "BULLISH",
            "BEARISH"
        }:
            confidence += 10

        if volume_activity in {
            "HIGH",
            "VERY HIGH"
        }:
            confidence += 5

        confidence = min(
            confidence,
            95
        )

        # -------------------------
        # DECISION
        # -------------------------

        signal = self.decision(
            momentum,
            book["pressure"],
            confidence
        )

        # -------------------------
        # RISK SCORE
        # -------------------------

        if signal == "HOLD":
            risk_score = 25
            risk_level = "LOW"

        elif confidence >= 80:
            risk_score = 35
            risk_level = "MEDIUM"

        else:
            risk_score = 55
            risk_level = "MEDIUM"

        # -------------------------
        # PAPER POSITION
        # -------------------------

        paper_allocation = 50.0

        quantity = (
            paper_allocation / price
            if price > 0
            else 0
        )

        # -------------------------
        # REASONING
        # -------------------------

        if signal == "BUY":

            reasoning = (
                f"BUY setup detected. "
                f"{book['pressure']} is supported by "
                f"{momentum} momentum. "
                f"Confidence is {confidence}%."
            )

        elif signal == "SELL":

            reasoning = (
                f"SELL setup detected. "
                f"{book['pressure']} is supported by "
                f"{momentum} momentum. "
                f"Confidence is {confidence}%."
            )

        else:

            reasoning = (
                f"HOLD: {book['pressure']} is not "
                f"confirmed by sufficiently strong "
                f"price momentum. Waiting for confirmation."
            )

        return {
            **market,

            "momentum": momentum,
            "momentum_score": momentum_score,

            "order_pressure": book["pressure"],
            "bid_share": book["bid_share"],
            "imbalance": book["imbalance"],

            "volume_activity": volume_activity,

            "market_regime": regime,

            "confidence": confidence,

            "risk_score": risk_score,
            "risk_level": risk_level,

            "signal": signal,

            "paper_allocation": paper_allocation,
            "quantity": quantity,

            "reasoning": reasoning
        }
