from mcp_servers.binance_mcp import BinanceMCPServer
from core.agent import AgenticAlphaOS

if __name__ == "__main__":
    agent = AgenticAlphaOS(BinanceMCPServer())
    result = agent.analyze("BTCUSDT")
    print(result)
