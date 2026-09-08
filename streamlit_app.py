import streamlit as st
import pandas as pd

from mcp_servers.binance_mcp import BinanceMCPServer
from core.agent import AgenticAlphaOS


# ==========================================
# PAGE
# ==========================================

st.set_page_config(
    page_title="Agentic Alpha",
    page_icon="ðŸ¤–",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("ðŸ¤– Agentic Alpha")

st.caption(
    "Autonomous Market Intelligence â€¢ Binance market data â€¢ Explainable agent reasoning"
)

st.markdown(
    """
    **Agentic Alpha** turns live market data into a structured decision:
    perception â†’ analysis â†’ multi-timeframe reasoning â†’ risk â†’ decision.
    """
)

s1, s2, s3 = st.columns(3)
s1.metric("DATA", "LIVE")
s2.metric("ENGINE", "AGENTIC ALPHA")
s3.metric("EXECUTION", "DISABLED")


# ==========================================
# MARKET CONTROLS
# ==========================================

st.subheader("âš™ï¸ Market Controls")

col1, col2 = st.columns([2, 1])

with col1:

    symbol = st.selectbox(
        "Select a trading pair",
        [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "SOLUSDT",
            "XRPUSDT"
        ]
    )

with col2:

    st.write("")

    st.write("")

    analyze = st.button(
        "ðŸ” Analyze Market",
        type="primary",
        use_container_width=True
    )


# ==========================================
# STATE
# ==========================================

if "result" not in st.session_state:
    st.session_state.result = None

if "error" not in st.session_state:
    st.session_state.error = None


# ==========================================
# RUN AGENT
# ==========================================

market = BinanceMCPServer()


if analyze:

    st.session_state.error = None

    try:

        agent = AgenticAlphaOS(
            market_adapter=market
        )

        with st.spinner(
            "ðŸ¤– Agent analyzing live Binance data..."
        ):

            result = agent.analyze(symbol)

        st.session_state.result = result

    except Exception as error:

        st.session_state.result = None

        st.session_state.error = str(error)


# ==========================================
# ERROR
# ==========================================

if st.session_state.error:

    st.error(
        "âŒ Market-data request failed."
    )

    st.code(
        st.session_state.error
    )

    st.stop()


result = st.session_state.result


# ==========================================
# RESULTS
# ==========================================

if result:

    st.divider()

    st.header(
        f"ðŸ“Š {result['symbol']} Market Intelligence"
    )


    # ======================================
    # MARKET METRICS
    # ======================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Price",
        f"${result['price']:,.4f}"
    )

    c2.metric(
        "24h Change",
        f"{result['change_percent']:+.2f}%"
    )

    c3.metric(
        "24h Volume",
        f"${result['volume']:,.0f}"
    )

    c4.metric(
        "Volume Activity",
        result["volume_activity"]
    )

    st.markdown("### ðŸŽ¯ Intelligence Snapshot")
    snap1, snap2, snap3, snap4 = st.columns(4)

    snap1.metric("Momentum", result["momentum"])
    snap2.metric("Order-Book", result["order_pressure"])
    snap3.metric("Regime", result["market_regime"])
    snap4.metric("Agent Signal", result["signal"])


    # ======================================
    # PRICE CHART
    # ======================================

    st.subheader("ðŸ“ˆ Live Price Chart")

    chart_interval = st.selectbox(
        "Chart timeframe",
        [
            "1m",
            "5m",
            "15m",
            "1h",
            "4h"
        ],
        index=1
    )

    try:

        chart_rows = market.get_klines(
            result["symbol"],
            chart_interval,
            100
        )

        chart_data = pd.DataFrame(
            chart_rows,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_base",
                "taker_quote",
                "ignore"
            ]
        )

        chart_data["time"] = pd.to_datetime(
            chart_data["open_time"],
            unit="ms"
        )

        chart_data["close"] = pd.to_numeric(
            chart_data["close"]
        )

        chart_data = chart_data[
            ["time", "close"]
        ].set_index("time")

        st.line_chart(
            chart_data,
            height=350
        )

    except Exception as error:

        st.warning(
            f"Chart unavailable: {error}"
        )


    st.divider()


    # ======================================
    # MULTI TIMEFRAME
    # ======================================

    st.subheader(
        "â±ï¸ Multi-Timeframe Momentum"
    )

    timeframe_rows = []

    for interval, data in result[
        "timeframes"
    ].items():

        timeframe_rows.append({
            "Timeframe": interval,
            "Momentum": data["momentum"],
            "Change": f"{data['change']:+.2f}%",
            "Score": data["score"]
        })

    st.dataframe(
        timeframe_rows,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Multi-Timeframe Score",
        f"{result['multi_score']:.0f}/100"
    )


    st.divider()


    # ======================================
    # MOMENTUM
    # ======================================

    st.subheader(
        "ðŸ“ˆ Momentum Engine"
    )

    m1, m2 = st.columns(2)

    m1.metric(
        "Momentum",
        result["momentum"]
    )

    m2.metric(
        "Momentum Score",
        f"{result['momentum_score']}/100"
    )

    st.progress(
        result["momentum_score"] / 100
    )


    st.divider()


    # ======================================
    # ORDER BOOK
    # ======================================

    st.subheader(
        "ðŸ“– Order-Book Intelligence"
    )

    o1, o2, o3 = st.columns(3)

    o1.metric(
        "Pressure",
        result["order_pressure"]
    )

    o2.metric(
        "Bid Share",
        f"{result['bid_share'] * 100:.1f}%"
    )

    o3.metric(
        "Imbalance",
        f"{result['imbalance'] * 100:+.1f}%"
    )


    st.divider()


    # ======================================
    # REGIME
    # ======================================

    st.subheader(
        "ðŸŒ Market Regime"
    )

    st.info(
        result["market_regime"]
    )


    st.divider()


    # ======================================
    # AGENT
    # ======================================

    st.subheader(
        "ðŸ¤– Agent Decision"
    )

    d1, d2 = st.columns(2)

    d1.metric(
        "Signal",
        result["signal"]
    )

    d2.metric(
        "Confidence",
        f"{result['confidence']}%"
    )

    st.progress(
        result["confidence"] / 100
    )

    st.markdown(
        f"**Decision logic:** {result['momentum']} momentum â€¢ "
        f"{result['order_pressure']} â€¢ "
        f"{result['volume_activity']} volume â€¢ "
        f"{result['market_regime']} regime"
    )


    st.subheader(
        "ðŸ§  Agent Reasoning"
    )

    st.info(
        result["reasoning"]
    )


    st.divider()


    # ======================================
    # RISK
    # ======================================

    st.subheader(
        "ðŸ›¡ï¸ Risk Engine"
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Risk Level",
        result["risk_level"]
    )

    r2.metric(
        "Risk Score",
        f"{result['risk_score']}/100"
    )

    r3.metric(
        "Allocation",
        f"${result['paper_allocation']:.2f}"
    )

    st.progress(
        result["risk_score"] / 100
    )


    st.divider()


    # ======================================
    # POSITION
    # ======================================

    st.subheader(
        "ðŸ“ Position Analysis"
    )

    p1, p2 = st.columns(2)

    p1.metric(
        "Suggested Allocation",
        f"${result['paper_allocation']:.2f}"
    )

    p2.metric(
        "Estimated Quantity",
        f"{result['quantity']:.8f}"
    )


    # ======================================
    # ORDER BOOK
    # ======================================

    with st.expander(
        "ðŸ“š View Order-Book Levels"
    ):

        left, right = st.columns(2)

        with left:

            st.write("ðŸŸ¢ Bids")

            st.dataframe(
                result["bids"][:10],
                use_container_width=True
            )

        with right:

            st.write("ðŸ”´ Asks")

            st.dataframe(
                result["asks"][:10],
                use_container_width=True
            )


    st.caption(
        "Live market data retrieved through the Binance public market-data adapter."
    )


else:

    # ======================================
    # LANDING
    # ======================================

    st.divider()

    st.subheader(
        "ðŸ§  Agentic Alpha Pipeline"
    )

    st.markdown(
        """
        **ðŸ“¡ PERCEPTION**

        Live Binance market data

        â†“

        **ðŸ“Š ANALYSIS**

        Price â€¢ Volume â€¢ Order Book

        â†“

        **â±ï¸ MULTI-TIMEFRAME**

        1m â€¢ 5m â€¢ 15m â€¢ 1h â€¢ 4h

        â†“

        **ðŸ§  REASONING**

        Momentum â€¢ Regime â€¢ Confidence

        â†“

        **ðŸ›¡ï¸ RISK**

        Risk Score â€¢ Position Sizing

        â†“

        **ðŸ¤– DECISION**

        BUY / SELL / HOLD
        """
    )

    st.divider()
    st.caption(
        "Agentic Alpha â€¢ Binance market intelligence â€¢ "
        "Human-controlled execution boundary"
    )
