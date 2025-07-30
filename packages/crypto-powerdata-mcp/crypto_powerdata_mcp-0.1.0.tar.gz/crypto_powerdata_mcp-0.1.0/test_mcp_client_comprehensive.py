#!/usr/bin/env python3
"""
Comprehensive MCP Client Test Suite
Tests all MCP service functionalities, including environment variable configuration
"""

import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPClientTester:
    """MCP Client Tester"""

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.test_results = []

    async def connect_to_server(self) -> bool:
        """Connects to the MCP server"""
        try:
            # Start MCP server process
            server_params = StdioServerParameters(
                command="python",
                args=["-m", "src.main"],
                env=None
            )

            # Create client session
            self.session = await stdio_client(server_params).__aenter__()

            # Initialize session
            await self.session.initialize()

            logger.info("✅ Successfully connected to MCP server")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to MCP server: {e}")
            return False

    async def disconnect(self):
        """Disconnects from the server"""
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
                logger.info("✅ Disconnected from MCP server")
            except Exception as e:
                logger.error(f"❌ Error disconnecting: {e}")

    async def test_server_info(self) -> Dict[str, Any]:
        """Tests server information retrieval"""
        test_name = "Server Information Retrieval"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Get server information
            result = await self.session.list_tools()

            tools = result.tools if hasattr(result, 'tools') else []
            tool_names = [tool.name for tool in tools]

            success = len(tools) > 0

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "tools_count": len(tools),
                    "tool_names": tool_names
                },
                "timestamp": datetime.now().isoformat()
            }

            if success:
                logger.info(f"✅ {test_name} successful - {len(tools)} tools found")
            else:
                logger.error(f"❌ {test_name} failed - No tools found")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_cex_price_basic(self) -> Dict[str, Any]:
        """Tests basic CEX price retrieval functionality"""
        test_name = "CEX Price Retrieval - Basic Functionality"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Call CEX price retrieval tool
            result = await self.session.call_tool(
                "get_cex_price",
                {
                    "exchange": "binance",
                    "symbol": "BTC/USDT"
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "exchange": "binance",
                    "symbol": "BTC/USDT",
                    "has_price": "price" in data.get("data", {}),
                    "response_keys": list(data.keys())
                },
                "timestamp": datetime.now().isoformat()
            }

            if success:
                price = data.get("data", {}).get("price")
                logger.info(f"✅ {test_name} successful - BTC/USDT price: ${price}")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_cex_price_with_fallback(self) -> Dict[str, Any]:
        """Tests CEX price retrieval with fallback exchanges"""
        test_name = "CEX Price Retrieval - Fallback Exchange"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Use a nonexistent primary exchange to test fallback mechanism
            result = await self.session.call_tool(
                "get_cex_price",
                {
                    "exchange": "nonexistent_exchange",
                    "symbol": "BTC/USDT",
                    "fallback_exchanges": ["binance", "coinbase"]
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "primary_exchange": "nonexistent_exchange",
                    "fallback_exchanges": ["binance", "coinbase"],
                    "actual_exchange": data.get("data", {}).get("exchange"),
                    "tried_exchanges": data.get("tried_exchanges", [])
                },
                "timestamp": datetime.now().isoformat()
            }

            if success:
                actual_exchange = data.get("data", {}).get("exchange")
                logger.info(f"✅ {test_name} successful - Using fallback exchange: {actual_exchange}")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_configure_env_vars(self) -> Dict[str, Any]:
        """Tests environment variable configuration functionality"""
        test_name = "Environment Variable Configuration"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Configure test environment variables
            test_env_vars = {
                "OKX_API_KEY": "test_api_key",
                "OKX_SECRET_KEY": "test_secret_key",
                "OKX_API_PASSPHRASE": "test_passphrase",
                "OKX_PROJECT_ID": "test_project_id",
                "RATE_LIMIT_REQUESTS_PER_SECOND": "5",
                "TIMEOUT_SECONDS": "60"
            }

            result = await self.session.call_tool(
                "configure_env_vars",
                {"env_vars": test_env_vars}
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "configured_vars": data.get("configured_vars", []),
                    "settings_summary": data.get("settings_summary", {}),
                    "env_vars_count": len(test_env_vars)
                },
                "timestamp": datetime.now().isoformat()
            }

            if success:
                logger.info(f"✅ {test_name} successful - Configured {len(test_env_vars)} environment variables")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_dex_data_basic(self) -> Dict[str, Any]:
        """Tests basic DEX data retrieval functionality"""
        test_name = "DEX Data Retrieval - Basic Functionality"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Test with a known token on Ethereum, without indicators
            result = await self.session.call_tool(
                "get_dex_data_with_indicators",
                {
                    "chain_index": "1",  # Ethereum
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
                    "timeframe": "1h",
                    "limit": 10
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "klines_count": len(data.get("data", {}).get("klines", [])),
                    "has_price_info": "price_info" in data.get("data", {})
                },
                "timestamp": datetime.now().isoformat()
            }

            if success:
                logger.info(f"✅ {test_name} successful - Retrieved {test_result['details']['klines_count']} k-lines")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_dex_data_without_credentials(self) -> Dict[str, Any]:
        """Tests DEX data retrieval behavior without API credentials"""
        test_name = "DEX Data Retrieval - Without Credentials"
        logger.info(f"🧪 Starting test: {test_name}")

        # Temporarily clear OKX credentials from environment for this test
        original_env = os.environ.copy()
        for key in ["OKX_API_KEY", "OKX_SECRET_KEY", "OKX_API_PASSPHRASE", "OKX_PROJECT_ID"]:
            if key in os.environ:
                del os.environ[key]

        try:
            result = await self.session.call_tool(
                "get_dex_data_with_indicators",
                {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "1h",
                    "limit": 5
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)
            error_message = data.get("error", "")

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "error_message": error_message
                },
                "timestamp": datetime.now().isoformat()
            }

            # Expecting an error about missing credentials
            if not success and ("credentials" in error_message.lower() or "api" in error_message.lower()):
                logger.info(f"✅ {test_name} successful - As expected, API credentials are required")
                test_result["success"] = True # Mark as success because it behaved as expected
            else:
                logger.error(f"❌ {test_name} failed - Unexpected behavior: {error_message}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        finally:
            # Restore original environment variables
            os.environ.clear()
            os.environ.update(original_env)

    async def test_dex_data_with_api_credentials(self) -> Dict[str, Any]:
        """Tests DEX data retrieval with API credentials"""
        test_name = "DEX Data Retrieval - With API Credentials"
        logger.info(f"🧪 Starting test: {test_name}")

        # Ensure credentials are set for this test (e.g., from .env loaded by main.py or explicitly set)
        # For testing, we might temporarily set dummy credentials if not already set by the test runner
        if not os.getenv("OKX_API_KEY"):
            logger.warning("⚠️  OKX API credentials not found in environment. Using dummy credentials for test.")
            os.environ["OKX_API_KEY"] = "dummy_api_key"
            os.environ["OKX_SECRET_KEY"] = "dummy_secret_key"
            os.environ["OKX_API_PASSPHRASE"] = "dummy_passphrase"
            os.environ["OKX_PROJECT_ID"] = "dummy_project_id"

        try:
            result = await self.session.call_tool(
                "get_dex_data_with_indicators",
                {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "1h",
                    "limit": 10
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "klines_count": len(data.get("data", {}).get("klines", [])),
                    "has_price_info": "price_info" in data.get("data", {})
                },
                "timestamp": datetime.now().isoformat()
            }

            if success and test_result['details']['klines_count'] > 0:
                logger.info(f"✅ {test_name} successful - Retrieved {test_result['details']['klines_count']} k-lines with credentials")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_get_dex_token_price(self) -> Dict[str, Any]:
        """Tests retrieving the current price of a DEX token"""
        test_name = "Get DEX Token Price"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            result = await self.session.call_tool(
                "get_dex_token_price",
                {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  # USDC
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "price": data.get("data", {}).get("price", "N/A")
                },
                "timestamp": datetime.now().isoformat()
            }

            if success and test_result['details']['price'] != "N/A":
                logger.info(f"✅ {test_name} successful - USDC Price: {test_result['details']['price']}")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_indicators_configuration(self) -> Dict[str, Any]:
        """Tests indicator configuration and retrieval for DEX data"""
        test_name = "DEX Data - Indicators Configuration"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Define a complex indicator configuration as a string
            indicators_config_str = json.dumps({
                "ema": [{"timeperiod": 12}, {"timeperiod": 26}, {"timeperiod": 120}],
                "macd": [{"fastperiod": 12, "slowperiod": 26, "signalperiod": 9}],
                "rsi": [{"timeperiod": 14}, {"timeperiod": 21}]
            })

            result = await self.session.call_tool(
                "get_enhanced_dex_data_with_indicators",
                {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "1h",
                    "limit": 100,
                    "indicators_config": indicators_config_str
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)
            metadata = data.get("data", {}).get("metadata", {})
            indicators_applied = metadata.get("indicators_applied", [])
            columns = metadata.get("columns", [])

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "indicators_applied": indicators_applied,
                    "columns_count": len(columns),
                    "has_ema_12": "ema_12" in columns,
                    "has_macd_output": any(col.startswith("macd") for col in columns),
                    "has_rsi_14": "rsi_14" in columns
                },
                "timestamp": datetime.now().isoformat()
            }

            if success and len(indicators_applied) > 0 and len(columns) > 5: # Basic columns + indicator columns
                logger.info(f"✅ {test_name} successful - Applied indicators: {indicators_applied}")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_get_available_indicators(self) -> Dict[str, Any]:
        """Tests retrieval of available indicators registry"""
        test_name = "Get Available Indicators"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            result = await self.session.call_tool(
                "get_available_indicators",
                {}
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)
            total_indicators = data.get("data", {}).get("total_indicators", 0)
            indicators_dict = data.get("data", {}).get("indicators", {})

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "total_indicators": total_indicators,
                    "registry_not_empty": bool(indicators_dict),
                    "has_sma": "sma" in indicators_dict,
                    "has_macd": "macd" in indicators_dict
                },
                "timestamp": datetime.now().isoformat()
            }

            if success and total_indicators > 50 and bool(indicators_dict):
                logger.info(f"✅ {test_name} successful - Found {total_indicators} indicators")
            else:
                logger.error(f"❌ {test_name} failed - {data.get('error', 'Unknown error')}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_error_handling_invalid_input(self) -> Dict[str, Any]:
        """Tests error handling with invalid input for tool calls"""
        test_name = "Error Handling - Invalid Input"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            # Example: call get_cex_price with missing symbol
            result = await self.session.call_tool(
                "get_cex_price",
                {
                    "exchange": "binance",
                    # "symbol": "BTC/USDT" # Missing symbol
                }
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)
            error_message = data.get("error", "")

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "error_message": error_message
                },
                "timestamp": datetime.now().isoformat()
            }

            # Expecting failure due to invalid input
            if not success and "missing required parameter" in error_message.lower():
                logger.info(f"✅ {test_name} successful - Expected error for invalid input: {error_message}")
                test_result["success"] = True # Mark as success because it behaved as expected
            else:
                logger.error(f"❌ {test_name} failed - Unexpected behavior: {error_message}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def test_error_handling_nonexistent_tool(self) -> Dict[str, Any]:
        """Tests error handling for calling a nonexistent tool"""
        test_name = "Error Handling - Nonexistent Tool"
        logger.info(f"🧪 Starting test: {test_name}")

        try:
            result = await self.session.call_tool(
                "nonexistent_tool",
                {}
            )

            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)

            success = data.get("success", False)
            error_message = data.get("error", "")

            test_result = {
                "test_name": test_name,
                "success": success,
                "details": {
                    "error_message": error_message
                },
                "timestamp": datetime.now().isoformat()
            }

            # Expecting failure due to nonexistent tool
            if not success and "tool not found" in error_message.lower():
                logger.info(f"✅ {test_name} successful - Expected error for nonexistent tool: {error_message}")
                test_result["success"] = True # Mark as success because it behaved as expected
            else:
                logger.error(f"❌ {test_name} failed - Unexpected behavior: {error_message}")

            return test_result

        except Exception as e:
            logger.error(f"❌ {test_name} exception: {e}")
            return {
                "test_name": test_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def run_all_tests(self) -> List[Dict[str, Any]]:
        """Runs all tests and returns a summary"""
        logger.info("🚀 Starting comprehensive MCP client test suite...")
        self.test_results = []

        if not await self.connect_to_server():
            self.test_results.append({
                "test_name": "Server Connection",
                "success": False,
                "details": "Failed to connect to MCP server",
                "timestamp": datetime.now().isoformat()
            })
            return self.test_results

        # Run individual tests
        self.test_results.append(await self.test_server_info())
        self.test_results.append(await self.test_cex_price_basic())
        self.test_results.append(await self.test_cex_price_with_fallback())
        self.test_results.append(await self.test_configure_env_vars())
        self.test_results.append(await self.test_dex_data_basic())
        self.test_results.append(await self.test_dex_data_without_credentials())
        self.test_results.append(await self.test_dex_data_with_api_credentials())
        self.test_results.append(await self.test_get_dex_token_price())
        self.test_results.append(await self.test_indicators_configuration())
        self.test_results.append(await self.test_get_available_indicators())
        self.test_results.append(await self.test_error_handling_invalid_input())
        self.test_results.append(await self.test_error_handling_nonexistent_tool())

        await self.disconnect()

        logger.info("📊 All tests completed.")
        return self.test_results

async def main():
    """Main function to run the comprehensive client tests"""
    tester = MCPClientTester()
    results = await tester.run_all_tests()

    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get("success"))

    logger.info("\n=== Comprehensive MCP Client Test Summary ===")
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        details = result.get("details", result.get("error", "N/A"))
        logger.info(f"{status} {result['test_name']} - Details: {details}")

    logger.info(f"\nOverall: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        logger.info("🎉 All comprehensive client tests passed successfully!")
        return True
    else:
        logger.error("⚠️  Some comprehensive client tests failed.")
        return False

if __name__ == "__main__":
    asyncio.run(main())
