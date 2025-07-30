#!/usr/bin/env python3
"""
Comprehensive MCP Server Testing Suite

This script performs detailed testing of the Crypto PowerData MCP service
including all enhanced features, transport protocols, and error handling.
"""

import asyncio
import json
import logging
import time
import aiohttp
import subprocess
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPServerTester:
    """Comprehensive MCP server testing suite"""
    
    def __init__(self):
        self.test_results = []
        self.server_process = None
        self.base_url = "http://localhost:8000"
        self.session_id = None
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", duration: float = 0):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "duration": f"{duration:.2f}s",
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        logger.info(f"{status} {test_name} ({duration:.2f}s) - {details}")
    
    async def test_enhanced_indicators_system(self):
        """Test the enhanced indicators system directly"""
        logger.info("🧪 Testing Enhanced Indicators System...")
        
        try:
            start_time = time.time()
            
            # Import and test enhanced indicators
            from src.enhanced_indicators import EnhancedTechnicalAnalysis
            from src.talib_registry import TALibRegistry
            import pandas as pd
            import numpy as np
            
            # Test registry
            registry = TALibRegistry()
            indicators = registry.get_all_indicators()
            
            if len(indicators) < 50:
                self.log_test_result(
                    "Enhanced Indicators - Registry", 
                    False, 
                    f"Expected 50+ indicators, got {len(indicators)}"
                )
                return
            
            # Test enhanced TA
            enhanced_ta = EnhancedTechnicalAnalysis()
            
            # Create sample data
            dates = pd.date_range(start='2024-01-01', periods=100, freq='1H')
            np.random.seed(42)
            prices = [50000 + i * 10 + np.random.normal(0, 100) for i in range(100)]
            
            sample_data = pd.DataFrame({
                'open': prices,
                'high': [p * 1.01 for p in prices],
                'low': [p * 0.99 for p in prices],
                'close': prices,
                'volume': [1000 + np.random.uniform(-100, 100) for _ in range(100)]
            }, index=dates)
            
            # Test multiple indicators with different parameters
            indicators_config = {
                'ema': [{'timeperiod': 12}, {'timeperiod': 26}, {'timeperiod': 50}],
                'rsi': [{'timeperiod': 14}, {'timeperiod': 21}],
                'macd': [{'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9}],
                'bbands': [{'timeperiod': 20, 'nbdevup': 2, 'nbdevdn': 2}],
                'sma': [{'timeperiod': 20}, {'timeperiod': 50}]
            }
            
            result = enhanced_ta.calculate_indicators(sample_data, indicators_config)
            
            # Verify results
            expected_columns = [
                'ema_12', 'ema_26', 'ema_50',
                'rsi_14', 'rsi_21',
                'macd_12_26_9_macd', 'macd_12_26_9_macdsignal', 'macd_12_26_9_macdhist',
                'bbands_2_2_20_upperband', 'bbands_2_2_20_middleband', 'bbands_2_2_20_lowerband',
                'sma_20', 'sma_50'
            ]
            
            missing_columns = [col for col in expected_columns if col not in result.columns]
            
            duration = time.time() - start_time
            
            if missing_columns:
                self.log_test_result(
                    "Enhanced Indicators - Calculation", 
                    False, 
                    f"Missing columns: {missing_columns}",
                    duration
                )
            else:
                self.log_test_result(
                    "Enhanced Indicators - Calculation", 
                    True, 
                    f"Successfully calculated {len(expected_columns)} indicator columns",
                    duration
                )
            
            # Test registry information
            self.log_test_result(
                "Enhanced Indicators - Registry", 
                True, 
                f"Registry contains {len(indicators)} indicators",
                duration
            )
            
        except Exception as e:
            self.log_test_result(
                "Enhanced Indicators - System", 
                False, 
                f"Error: {str(e)}"
            )
    
    async def start_http_server(self):
        """Start HTTP server for testing"""
        logger.info("🚀 Starting HTTP server...")
        
        try:
            # Start the dual transport server in HTTP mode
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "src.dual_transport_server",
                "--mode", "http", "--port", "8000", "--host", "127.0.0.1"
            ], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            await asyncio.sleep(3)
            
            # Test if server is running
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"{self.base_url}/health") as resp:
                        if resp.status == 200:
                            self.log_test_result(
                                "HTTP Server - Startup", 
                                True, 
                                "Server started successfully"
                            )
                            return True
                        else:
                            self.log_test_result(
                                "HTTP Server - Startup", 
                                False, 
                                f"Health check failed: {resp.status}"
                            )
                            return False
                except Exception as e:
                    self.log_test_result(
                        "HTTP Server - Startup", 
                        False, 
                        f"Connection failed: {str(e)}"
                    )
                    return False
                    
        except Exception as e:
            self.log_test_result(
                "HTTP Server - Startup", 
                False, 
                f"Failed to start server: {str(e)}"
            )
            return False
    
    async def test_http_transport(self):
        """Test HTTP transport protocol"""
        logger.info("🌐 Testing HTTP Transport...")
        
        async with aiohttp.ClientSession() as session:
            try:
                start_time = time.time()
                
                # Test initialization
                init_request = {
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0.0"}
                    },
                    "id": 1
                }
                
                async with session.post(f"{self.base_url}/mcp", json=init_request) as resp:
                    if resp.status == 200:
                        self.session_id = resp.headers.get("Mcp-Session-Id")
                        result = await resp.json()
                        
                        duration = time.time() - start_time
                        
                        if "result" in result and "serverInfo" in result["result"]:
                            self.log_test_result(
                                "HTTP Transport - Initialize", 
                                True, 
                                f"Session ID: {self.session_id}",
                                duration
                            )
                        else:
                            self.log_test_result(
                                "HTTP Transport - Initialize", 
                                False, 
                                f"Invalid response: {result}",
                                duration
                            )
                    else:
                        self.log_test_result(
                            "HTTP Transport - Initialize", 
                            False, 
                            f"HTTP {resp.status}"
                        )
                
            except Exception as e:
                self.log_test_result(
                    "HTTP Transport - Initialize", 
                    False, 
                    f"Error: {str(e)}"
                )
    
    async def test_tools_list(self):
        """Test tools listing"""
        logger.info("🔧 Testing Tools List...")
        
        async with aiohttp.ClientSession() as session:
            try:
                start_time = time.time()
                
                tools_request = {
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {},
                    "id": 2
                }
                
                headers = {"Mcp-Session-Id": self.session_id} if self.session_id else {}
                
                async with session.post(f"{self.base_url}/mcp", json=tools_request, headers=headers) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        duration = time.time() - start_time
                        
                        if "result" in result and "tools" in result["result"]:
                            tools = result["result"]["tools"]
                            tool_names = [tool["name"] for tool in tools]
                            
                            expected_tools = [
                                "get_enhanced_dex_data_with_indicators",
                                "get_available_indicators",
                                "get_cex_data_with_indicators",
                                "get_dex_data_with_indicators"
                            ]
                            
                            missing_tools = [tool for tool in expected_tools if tool not in tool_names]
                            
                            if missing_tools:
                                self.log_test_result(
                                    "Tools - List", 
                                    False, 
                                    f"Missing tools: {missing_tools}",
                                    duration
                                )
                            else:
                                self.log_test_result(
                                    "Tools - List", 
                                    True, 
                                    f"Found {len(tools)} tools: {tool_names}",
                                    duration
                                )
                        else:
                            self.log_test_result(
                                "Tools - List", 
                                False, 
                                f"Invalid response: {result}",
                                duration
                            )
                    else:
                        self.log_test_result(
                            "Tools - List", 
                            False, 
                            f"HTTP {resp.status}"
                        )
                        
            except Exception as e:
                self.log_test_result(
                    "Tools - List", 
                    False, 
                    f"Error: {str(e)}"
                )
    
    async def test_get_available_indicators(self):
        """Test get_available_indicators tool"""
        logger.info("📊 Testing Get Available Indicators...")
        
        async with aiohttp.ClientSession() as session:
            try:
                start_time = time.time()
                
                tool_request = {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "get_available_indicators",
                        "arguments": {}
                    },
                    "id": 3
                }
                
                headers = {"Mcp-Session-Id": self.session_id} if self.session_id else {}
                
                async with session.post(f"{self.base_url}/mcp", json=tool_request, headers=headers) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        duration = time.time() - start_time
                        
                        if "result" in result:
                            # Parse the content
                            content = result["result"].get("content", [])
                            if content and len(content) > 0:
                                text_content = content[0].get("text", "")
                                try:
                                    data = json.loads(text_content)
                                    if "success" in data and data["success"]:
                                        indicators_count = len(data["data"]["indicators"])
                                        categories_count = len(data["data"]["categories"])
                                        
                                        self.log_test_result(
                                            "Tools - Get Available Indicators", 
                                            True, 
                                            f"Found {indicators_count} indicators in {categories_count} categories",
                                            duration
                                        )
                                    else:
                                        self.log_test_result(
                                            "Tools - Get Available Indicators", 
                                            False, 
                                            f"Tool returned error: {data.get('error', 'Unknown error')}",
                                            duration
                                        )
                                except json.JSONDecodeError:
                                    self.log_test_result(
                                        "Tools - Get Available Indicators", 
                                        False, 
                                        "Invalid JSON response",
                                        duration
                                    )
                            else:
                                self.log_test_result(
                                    "Tools - Get Available Indicators", 
                                    False, 
                                    "Empty content in response",
                                    duration
                                )
                        else:
                            self.log_test_result(
                                "Tools - Get Available Indicators", 
                                False, 
                                f"Invalid response: {result}",
                                duration
                            )
                    else:
                        self.log_test_result(
                            "Tools - Get Available Indicators", 
                            False, 
                            f"HTTP {resp.status}"
                        )
                        
            except Exception as e:
                self.log_test_result(
                    "Tools - Get Available Indicators", 
                    False, 
                    f"Error: {str(e)}"
                )
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.server_process:
            logger.info("🧹 Cleaning up server process...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
    
    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "="*80)
        logger.info("📋 TEST SUMMARY")
        logger.info("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests} ✅")
        logger.info(f"Failed: {failed_tests} ❌")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        logger.info("\n📊 DETAILED RESULTS:")
        for result in self.test_results:
            logger.info(f"{result['status']} {result['test']} ({result['duration']}) - {result['details']}")
        
        if failed_tests > 0:
            logger.info("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    logger.info(f"  • {result['test']}: {result['details']}")
        
        logger.info("\n" + "="*80)
    
    async def run_all_tests(self):
        """Run all tests"""
        logger.info("🚀 Starting Comprehensive MCP Server Testing...")
        logger.info("="*80)
        
        try:
            # Test 1: Enhanced Indicators System
            await self.test_enhanced_indicators_system()
            
            # Test 2: HTTP Server Startup
            server_started = await self.start_http_server()
            
            if server_started:
                # Test 3: HTTP Transport
                await self.test_http_transport()
                
                # Test 4: Tools List
                await self.test_tools_list()
                
                # Test 5: Get Available Indicators
                await self.test_get_available_indicators()
            
        except Exception as e:
            logger.error(f"Critical error during testing: {e}")
        
        finally:
            await self.cleanup()
            self.print_summary()


async def main():
    """Main test runner"""
    tester = MCPServerTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
