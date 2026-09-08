import streamlit as st
import pandas as pd

from mcp_servers.binance_mcp import BinanceMCPServer
from core.agent import AgenticAlphaOS


# ==========================================
# PAGE
# ==========================================

st.set_page_config(
    page_title="Agentic Alpha",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("🤖 Agentic Alpha")

st.caption(
    "Binance Agent OS • MCP-ready autonomous market intelligence"
)


# ==========================================
# MARKET CONTROLS
# ==========================================

st.subheader("⚙️ Market Controls")

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
        "🔍 Analyze Market",
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

if analyze:

    st.session_state.error = None

    try:

        market = BinanceMCPServer()

        agent = AgenticAlphaOS(
            market_adapter=market
        )

        with st.spinner(
            "🤖 Agent analyzing live Binance data..."
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
        "❌ Market-data request failed."
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
        f"📊 {result['symbol']} Market Intelligence"
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


    # ======================================
    # PRICE CHART
    # ======================================

    st.subheader("📈 Live Price Chart")

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
        "⏱️ Multi-Timeframe Momentum"
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
        "📈 Momentum Engine"
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
        "📖 Order-Book Intelligence"
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
        "🌐 Market Regime"
    )

    st.info(
        result["market_regime"]
    )


    st.divider()


    # ======================================
    # AGENT
    # ======================================

    st.subheader(
        "🤖 Agent Decision"
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


    st.subheader(
        "🧠 Agent Reasoning"
    )

    st.info(
        result["reasoning"]
    )


    st.divider()


    # ======================================
    # RISK
    # ======================================

    st.subheader(
        "🛡️ Risk Engine"
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
        "📐 Position Analysis"
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
        "📚 View Order-Book Levels"
    ):

        left, right = st.columns(2)

        with left:

            st.write("🟢 Bids")

            st.dataframe(
                result["bids"][:10],
                use_container_width=True
            )

        with right:

            st.write("🔴 Asks")

            st.dataframe(
                result["asks"][:10],
                use_container_width=True
            )


    st.caption(
        f"Market-data endpoint: "
        f"{result['endpoint']}"
    )


else:

    # ======================================
    # LANDING
    # ======================================

    st.divider()

    st.subheader(
        "🧠 Agentic Alpha Pipeline"
    )

    st.markdown(
        """
        **📡 PERCEPTION**

        Live Binance market data

        ↓

        **📊 ANALYSIS**

        Price • Volume • Order Book

        ↓

        **⏱️ MULTI-TIMEFRAME**

        1m • 5m • 15m • 1h • 4h

        ↓

        **🧠 REASONING**

        Momentum • Regime • Confidence

        ↓

        **🛡️ RISK**

        Risk Score • Position Sizing

        ↓

        **🤖 DECISION**

        BUY / SELL / HOLD
        """
    )
