class AgenticAlphaOS:

    def __init__(self, market_adapter):
        self.market = market_adapter

    # ==========================================
    # ORDER BOOK ANALYSIS
    # ==========================================

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

    # ==========================================
    # MOMENTUM
    # ==========================================

    @staticmethod
    def momentum_analysis(change):

        if change >= 3:
            return "STRONG BULLISH", 90

        elif change >= 1:
            return "BULLISH", 75

        elif change > 0.25:
            return "MILD BULLISH", 60

        elif change <= -3:
            return "STRONG BEARISH", 10

        elif change <= -1:
            return "BEARISH", 25

        elif change < -0.25:
            return "MILD BEARISH", 40

        return "NEUTRAL", 50

    # ==========================================
    # VOLUME
    # ==========================================

    @staticmethod
    def volume_analysis(volume):

        if volume >= 1_000_000_000:
            return "VERY HIGH"

        elif volume >= 500_000_000:
            return "HIGH"

        elif volume >= 100_000_000:
            return "NORMAL"

        return "LOW"

    # ==========================================
    # MARKET REGIME
    # ==========================================

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

        if (
            momentum in bullish
            and pressure == "BUY PRESSURE"
        ):
            return "BULLISH TREND"

        if (
            momentum in bearish
            and pressure == "SELL PRESSURE"
        ):
            return "BEARISH TREND"

        if momentum == "NEUTRAL":
            return "RANGING / NEUTRAL"

        return "MIXED / TRANSITION"

    # ==========================================
    # CONFIDENCE
    # ==========================================

    @staticmethod
    def calculate_confidence(
        momentum,
        pressure,
        volume_activity
    ):

        confidence = 50

        # Order-book confirmation
        if pressure in {
            "BUY PRESSURE",
            "SELL PRESSURE"
        }:
            confidence += 15

        # Momentum strength
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

        # Volume confirmation
        if volume_activity == "VERY HIGH":
            confidence += 10

        elif volume_activity == "HIGH":
            confidence += 5

        return min(confidence, 95)

    # ==========================================
    # DECISION
    # ==========================================

    @staticmethod
    def make_decision(
        momentum,
        pressure,
        confidence
    ):

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

    # ==========================================
    # RISK
    # ==========================================

    @staticmethod
    def risk_analysis(
        signal,
        confidence,
        change
    ):

        if signal == "HOLD":
            return 25, "LOW"

        if abs(change) >= 5:
            return 75, "HIGH"

        if confidence >= 80:
            return 35, "MEDIUM"

        return 50, "MEDIUM"

    # ==========================================
    # REASONING
    # ==========================================

    @staticmethod
    def generate_reasoning(
        momentum,
        pressure,
        volume_activity,
        regime,
        signal,
        confidence
    ):

        if signal == "BUY":

            return (
                f"BUY setup detected. "
                f"Price momentum is {momentum.lower()} "
                f"and the order book shows {pressure.lower()}. "
                f"Volume activity is {volume_activity.lower()}, "
                f"providing additional confirmation. "
                f"The current market regime is {regime.lower()}. "
                f"Decision confidence is {confidence}%."
            )

        if signal == "SELL":

            return (
                f"SELL setup detected. "
                f"Price momentum is {momentum.lower()} "
                f"and the order book shows {pressure.lower()}. "
                f"Volume activity is {volume_activity.lower()}. "
                f"The current market regime is {regime.lower()}. "
                f"Decision confidence is {confidence}%."
            )

        return (
            f"HOLD decision. The current combination of "
            f"{momentum.lower()} momentum and "
            f"{pressure.lower()} does not provide enough "
            f"confirmation for an executable directional signal. "
            f"The agent is waiting for stronger confirmation."
        )

    # ==========================================
    # COMPLETE ANALYSIS
    # ==========================================

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
        volume_activity = (
            self.volume_analysis(volume)
        )

        # Market regime
        regime = self.market_regime(
            momentum,
            book["pressure"]
        )

        # Confidence
        confidence = self.calculate_confidence(
            momentum,
            book["pressure"],
            volume_activity
        )

        # Decision
        signal = self.make_decision(
            momentum,
            book["pressure"],
            confidence
        )

        # Risk
        risk_score, risk_level = (
            self.risk_analysis(
                signal,
                confidence,
                change
            )
        )

        # Paper allocation
        paper_allocation = 50.0

        quantity = (
            paper_allocation / price
            if price > 0
            else 0
        )

        # Reasoning
        reasoning = self.generate_reasoning(
            momentum,
            book["pressure"],
            volume_activity,
            regime,
            signal,
            confidence
        )

        return {

            **market,

            "momentum": momentum,

            "momentum_score": momentum_score,

            "order_pressure":
                book["pressure"],

            "bid_share":
                book["bid_share"],

            "imbalance":
                book["imbalance"],

            "volume_activity":
                volume_activity,

            "market_regime":
                regime,

            "confidence":
                confidence,

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "signal":
                signal,

            "paper_allocation":
                paper_allocation,

            "quantity":
                quantity,

            "reasoning":
                reasoning
        }
