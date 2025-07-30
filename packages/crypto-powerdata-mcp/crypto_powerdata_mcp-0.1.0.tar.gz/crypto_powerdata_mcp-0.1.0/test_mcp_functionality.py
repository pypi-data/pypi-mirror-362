import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """
    Tests the crypto-powerdata-mcp server functionality.
    """
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "src.main"],
        cwd=".",
        env={"PYTHONPATH": "."}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("MCP Server Initialized.")

            # Test Case 1: Get CEX Data with Indicators
            print("\n--- Testing get_cex_data_with_indicators ---")
            cex_data_result = await session.call_tool(
                "get_cex_data_with_indicators",
                {
                    "exchange": "binance",
                    "symbol": "BTC/USDT",
                    "timeframe": "1h",
                    "limit": 50,
                    "indicators_config": {
                        "sma": {"period": 20},
                        "rsi": {"period": 14}
                    }
                }
            )
            print("CEX Data Result:")
            print(json.dumps(json.loads(cex_data_result.content[0].text), indent=2))

            # Test Case 2: Get DEX Token Price
            print("\n--- Testing get_dex_token_price ---")
            dex_price_result = await session.call_tool(
                "get_dex_token_price",
                {
                    "chain_index": "1",  # Ethereum
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
                }
            )
            print("DEX Price Result:")
            print(json.dumps(json.loads(dex_price_result.content[0].text), indent=2))

            # Test Case 3: Get DEX Data with Indicators
            print("\n--- Testing get_dex_data_with_indicators ---")
            dex_data_result = await session.call_tool(
                "get_dex_data_with_indicators",
                {
                    "chain_index": "1",  # Ethereum
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
                    "timeframe": "1h",
                    "limit": 50,
                    "indicators_config": {
                        "sma": {"period": 20},
                        "rsi": {"period": 14}
                    }
                }
            )
            print("DEX Data Result:")
            # The result is a JSON string, so we parse it for pretty printing
            print(json.dumps(json.loads(dex_data_result.content[0].text), indent=2))

if __name__ == "__main__":
    asyncio.run(test_mcp_server())