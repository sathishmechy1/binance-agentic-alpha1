class AgenticAlphaOS:

    def __init__(self, market_adapter):
        self.market = market_adapter

    # ==========================================
    # MOMENTUM
    # ==========================================

    @staticmethod
    def momentum_from_change(change):

        if change >= 2:
            return "STRONG BULLISH", 90

        if change >= 0.75:
            return "BULLISH", 75

        if change > 0.15:
            return "MILD BULLISH", 60

        if change <= -2:
            return "STRONG BEARISH", 10

        if change <= -0.75:
            return "BEARISH", 25

        if change < -0.15:
            return "MILD BEARISH", 40

        return "NEUTRAL", 50

    # ==========================================
    # ORDER BOOK
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

        if total == 0:

            return {
                "bid_share": 0.5,
                "imbalance": 0,
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
    # VOLUME
    # ==========================================

    @staticmethod
    def volume_activity(volume):

        if volume >= 1_000_000_000:
            return "VERY HIGH"

        if volume >= 500_000_000:
            return "HIGH"

        if volume >= 100_000_000:
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

        if momentum in bullish and pressure == "BUY PRESSURE":
            return "BULLISH TREND"

        if momentum in bearish and pressure == "SELL PRESSURE":
            return "BEARISH TREND"

        if momentum == "NEUTRAL":
            return "RANGING / NEUTRAL"

        return "MIXED / TRANSITION"

    # ==========================================
    # KLINE MOMENTUM
    # ==========================================

    def timeframe_analysis(
        self,
        symbol,
        interval
    ):

        rows = self.market.get_klines(
            symbol,
            interval,
            50
        )

        closes = [
            float(row[4])
            for row in rows
        ]

        if len(closes) < 2:

            return {
                "interval": interval,
                "change": 0,
                "momentum": "NEUTRAL",
                "score": 50
            }

        first = closes[0]
        last = closes[-1]

        change = (
            (last - first) / first
        ) * 100

        momentum, score = (
            self.momentum_from_change(change)
        )

        return {
            "interval": interval,
            "change": change,
            "momentum": momentum,
            "score": score
        }

    # ==========================================
    # DECISION
    # ==========================================

    @staticmethod
    def decision(
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
    # COMPLETE ANALYSIS
    # ==========================================

    def analyze(self, symbol):

        market = self.market.get_market_data(
            symbol
        )

        price = market["price"]

        change = market["change_percent"]

        volume = market["volume"]

        # Order book
        book = self.order_book_analysis(
            market["bids"],
            market["asks"]
        )

        # Main momentum
        momentum, momentum_score = (
            self.momentum_from_change(change)
        )

        # Volume
        volume_level = self.volume_activity(
            volume
        )

        # Timeframes
        timeframes = {}

        for interval in [
            "1m",
            "5m",
            "15m",
            "1h",
            "4h"
        ]:

            try:

                timeframes[interval] = (
                    self.timeframe_analysis(
                        symbol,
                        interval
                    )
                )

            except Exception:

                timeframes[interval] = {
                    "interval": interval,
                    "change": 0,
                    "momentum": "UNAVAILABLE",
                    "score": 50
                }

        # Average timeframe score
        valid_scores = [
            item["score"]
            for item in timeframes.values()
            if item["momentum"] != "UNAVAILABLE"
        ]

        if valid_scores:

            multi_score = (
                sum(valid_scores)
                / len(valid_scores)
            )

        else:

            multi_score = 50

        # Market regime
        regime = self.market_regime(
            momentum,
            book["pressure"]
        )

        # Confidence
        confidence = 50

        if book["pressure"] != "BALANCED":
            confidence += 15

        if momentum in {
            "BULLISH",
            "BEARISH"
        }:
            confidence += 10

        if momentum in {
            "STRONG BULLISH",
            "STRONG BEARISH"
        }:
            confidence += 20

        if volume_level in {
            "HIGH",
            "VERY HIGH"
        }:
            confidence += 5

        # Multi-timeframe confirmation
        if multi_score >= 65:
            confidence += 5

        elif multi_score <= 35:
            confidence += 5

        confidence = min(
            confidence,
            95
        )

        # Decision
        signal = self.decision(
            momentum,
            book["pressure"],
            confidence
        )

        # Risk
        if signal == "HOLD":

            risk_score = 25
            risk_level = "LOW"

        elif abs(change) >= 5:

            risk_score = 75
            risk_level = "HIGH"

        else:

            risk_score = 45
            risk_level = "MEDIUM"

        # Paper sizing
        allocation = 50.0

        quantity = (
            allocation / price
            if price > 0
            else 0
        )

        # Reasoning
        if signal == "BUY":

            reasoning = (
                "Bullish confirmation detected across "
                f"price momentum and {book['pressure'].lower()}. "
                f"Multi-timeframe score is "
                f"{multi_score:.0f}/100. "
                f"Confidence is {confidence}%."
            )

        elif signal == "SELL":

            reasoning = (
                "Bearish confirmation detected across "
                f"price momentum and {book['pressure'].lower()}. "
                f"Multi-timeframe score is "
                f"{multi_score:.0f}/100. "
                f"Confidence is {confidence}%."
            )

        else:

            reasoning = (
                f"HOLD: {book['pressure'].lower()} "
                f"is not sufficiently confirmed by "
                f"price momentum. "
                f"Multi-timeframe score is "
                f"{multi_score:.0f}/100. "
                "The agent is waiting for stronger confirmation."
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
                volume_level,

            "market_regime":
                regime,

            "timeframes":
                timeframes,

            "multi_score":
                multi_score,

            "confidence":
                confidence,

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "signal":
                signal,

            "paper_allocation":
                allocation,

            "quantity":
                quantity,

            "reasoning":
                reasoning
        }
