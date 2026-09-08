import streamlit as st

from mcp_servers.binance_mcp import BinanceMCPServer
from core.agent import AgenticAlphaOS


# ==========================================
# PAGE CONFIG
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
    "Binance Agent OS • MCP-ready market intelligence"
)

st.warning(
    "🛡️ READ-ONLY / PAPER TRADING MODE — "
    "No Binance orders are placed."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Agent Controls")

symbol = st.sidebar.selectbox(
    "Trading Pair",
    [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "SOLUSDT",
        "XRPUSDT"
    ]
)

analyze = st.sidebar.button(
    "🔍 Analyze Market",
    type="primary",
    use_container_width=True
)


# ==========================================
# SESSION STATE
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
            "🤖 Agent analyzing Binance market data..."
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
        "❌ Binance market-data request failed."
    )

    st.code(
        st.session_state.error
    )

    st.info(
        "The application automatically tried "
        "multiple public Binance market-data endpoints."
    )

    st.stop()


# ==========================================
# RESULT
# ==========================================

result = st.session_state.result


if result:

    # ======================================
    # MARKET
    # ======================================

    st.header(
        f"📊 {result['symbol']} Market Intelligence"
    )

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

    st.divider()


    # ======================================
    # MOMENTUM
    # ======================================

    st.subheader("📈 Momentum")

    m1, m2 = st.columns(2)

    m1.metric(
        "Momentum",
        result["momentum"]
    )

    m2.metric(
        "Momentum Score",
        f"{result['momentum_score']}/100"
    )

    st.divider()


    # ======================================
    # ORDER BOOK
    # ======================================

    st.subheader("📖 Order-Book Intelligence")

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
    # MARKET REGIME
    # ======================================

    st.subheader("🌐 Market Regime")

    st.info(
        result["market_regime"]
    )

    st.divider()


    # ======================================
    # AGENT DECISION
    # ======================================

    st.subheader("🤖 Agent Decision")

    d1, d2 = st.columns(2)

    d1.metric(
        "Signal",
        result["signal"]
    )

    d2.metric(
        "Confidence",
        f"{result['confidence']}%"
    )

    st.write("**Agent Reasoning:**")

    st.info(
        result["reasoning"]
    )

    st.divider()


    # ======================================
    # RISK ENGINE
    # ======================================

    st.subheader("🛡️ Risk Engine")

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
        "Paper Allocation",
        f"${result['paper_allocation']:.2f}"
    )

    st.success(
        "Risk engine active. "
        "Real execution is disabled."
    )

    st.divider()


    # ======================================
    # PAPER EXECUTION
    # ======================================

    st.subheader("🧪 Paper Execution")

    st.write(
        f"**Decision:** {result['signal']}"
    )

    st.write(
        f"**Paper Allocation:** "
        f"${result['paper_allocation']:.2f}"
    )

    st.write(
        f"**Estimated Quantity:** "
        f"{result['quantity']:.8f}"
    )

    st.info(
        "No real Binance order was submitted."
    )

    st.divider()


    # ======================================
    # ORDER BOOK DETAILS
    # ======================================

    with st.expander(
        "📚 View Top Order-Book Levels"
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


    # ======================================
    # DATA SOURCE
    # ======================================

    st.caption(
        f"Data endpoint: {result['endpoint']}"
    )

else:

    st.info(
        "Select a trading pair and press "
        "**Analyze Market**."
    )

    st.markdown(
        """
        ### 🧠 Agentic Alpha Pipeline

        **PERCEPTION**

        Live Binance market data

        ↓

        **ANALYSIS**

        Price • Volume • Momentum • Order Book

        ↓

        **REASONING**

        Market regime + confidence

        ↓

        **RISK**

        Risk score + allocation

        ↓

        **DECISION**

        BUY / SELL / HOLD

        ↓

        **EXECUTION**

        Paper trading only
        """
    )
