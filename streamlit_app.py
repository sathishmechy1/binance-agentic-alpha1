import streamlit as st
from mcp_servers.binance_mcp import BinanceMCPServer
from core.agent import AgenticAlphaOS

st.set_page_config(page_title="Agentic Alpha", page_icon="🤖", layout="wide")

st.title("🤖 Agentic Alpha")
st.caption("Binance Agent OS-style market analysis • Read-only / paper trading")

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
symbol = st.selectbox("Trading pair", symbols)

if st.button("🔄 Analyze Market", type="primary"):
    try:
        agent = AgenticAlphaOS(BinanceMCPServer())
        result = agent.analyze(symbol)
        st.session_state["result"] = result
    except Exception as e:
        st.error(f"Binance market-data request failed: {e}")

result = st.session_state.get("result")

if result:
    st.subheader(result["symbol"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Price", f"${result['price']:,.4f}")
    c2.metric("24h Change", f"{result['change_percent']:+.2f}%")
    c3.metric("24h Volume", f"${result['volume']:,.0f}")
    c4.metric("Range", f"${result['low']:,.4f} – ${result['high']:,.4f}")

    st.divider()
    a, b, c, d = st.columns(4)
    a.metric("Momentum", result["momentum"])
    b.metric("Order Pressure", result["order_pressure"])
    c.metric("Bid Share", f"{result['order_book_ratio']*100:.1f}%")
    d.metric("Agent Signal", result["signal"])

    st.subheader("Risk Engine")
    if result["risk_ok"]:
        st.success(result["risk_reason"])
    else:
        st.warning(result["risk_reason"])

    st.write(
        f"Paper allocation: **${result['suggested_usdt']:.2f}**  |  "
        f"Estimated quantity: **{result['quantity']:.8f} {result['symbol'].replace('USDT','')}**"
    )

    st.info(
        "Execution is intentionally disabled. The dashboard uses public Binance "
        "market data and produces paper-trading decisions only."
    )

    with st.expander("Top order-book levels"):
        st.write("Bids")
        st.dataframe(result["bids"][:10], use_container_width=True)
        st.write("Asks")
        st.dataframe(result["asks"][:10], use_container_width=True)
else:
    st.info("Choose a pair and press Analyze Market.")
