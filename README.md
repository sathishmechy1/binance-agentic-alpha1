# 🤖 Agentic Alpha

A hackathon-ready, read-only prototype for a Binance Agent OS / MCP trading-agent concept.

## What it does

- Pulls live public Binance Spot market data
- Shows price, 24h change, volume, high/low
- Calculates order-book pressure
- Classifies simple momentum
- Produces BUY / SELL / HOLD paper-trading signals
- Applies a configurable paper risk limit
- Provides a Streamlit dashboard
- Keeps authenticated order execution disabled

## Architecture

Streamlit UI
→ AgenticAlphaOS
→ Binance market-data adapter
→ Risk Engine
→ Paper decision

The `mcp_servers/` directory is structured.

## Run locally

```bash
git clone https://github.com/YOUR_USERNAME/binance-agentic-alpha.git
cd binance-agentic-alpha
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Windows activation:

```bash
.venv\Scripts\activate
```

No Binance API key is required for the current read-only dashboard.

## Streamlit Cloud

1. Push the repository to GitHub.
2. Create a new Streamlit app.
3. Select `streamlit_app.py` as the main file.
4. Deploy.

No secrets are required for the current public market-data version.

## Safety

This version does not place orders and does not request trading permissions. Do not add real Binance secrets to GitHub.

## Hackathon positioning

The project demonstrates an agent loop:

**Perception → Analysis → Risk Check → Decision → Paper Execution**

For a final submission, connect the perception and action layers to the official Binance MCP/Agent OS environment required by the competition, and replace the placeholder sentiment adapter with a real, documented data source.
