#!/usr/bin/env python3
"""
Test Script: Validates Crypto PowerData MCP Service Functionality

This script tests two core functionalities:
1. CEX real-time price retrieval
2. DEX K-line data retrieval (with custom technical indicators)
"""

import asyncio
import json
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_provider import get_klines_with_custom_indicators
import ccxt


async def test_cex_price_fetch():
    """Tests CEX real-time price retrieval functionality"""
    print("=== Testing CEX Real-time Price Retrieval ===")

    try:
        # Test Binance
        exchange = ccxt.binance()
        symbol = 'BTC/USDT'

        if exchange.has.get('fetchTicker'):
            ticker = exchange.fetch_ticker(symbol)

            print(f"✅ Successfully retrieved {symbol} price data:")
            print(f"   Exchange: Binance")
            print(f"   Current Price: ${ticker.get('last', 'N/A')}")
            print(f"   24h High: ${ticker.get('high', 'N/A')}")
            print(f"   24h Low: ${ticker.get('low', 'N/A')}")
            print(f"   24h Volume: {ticker.get('baseVolume', 'N/A')}")
            print(f"   24h Change: {ticker.get('percentage', 'N/A')}%")
            return True
        else:
            print("❌ Binance does not support fetchTicker")
            return False

    except Exception as e:
        print(f"❌ CEX price retrieval test failed: {e}")
        return False


async def test_dex_klines_with_indicators():
    """Tests DEX K-line data retrieval (with custom technical indicators)"""
    print("\n=== Testing DEX K-line Data Retrieval (with Custom Technical Indicators) ===")

    try:
        # Custom indicator configuration
        indicators_config = {
            'macd': {'fast': 12, 'slow': 26, 'signal': 9},
            'rsi': {'period': 14},
            'bb': {'period': 20, 'std': 2},
            'sma': {'period': 20},
            'ema': {'period': 50},
            'stoch': {'k_period': 14, 'd_period': 3}
        }

        # Get K-line data
        exchange = 'binance'
        symbol = 'BTC/USDT'
        timeframe = '1h'
        limit = 50

        print(f"Retrieving {timeframe} K-line data for {symbol}...")
        print(f"Indicator configuration: {list(indicators_config.keys())}")

        data = await get_klines_with_custom_indicators(
            exchange, symbol, timeframe, limit, indicators_config
        )

        if data is not None and not data.empty:
            print(f"✅ Successfully retrieved {len(data)} K-line data")

            # Display basic information
            latest = data.iloc[-1]
            print(f"   Latest Price: ${latest['close']:.2f}")
            print(f"   Latest Time: {data.index[-1]}")

            # Display calculated indicators
            indicator_columns = [col for col in data.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
            print(f"   Number of Calculated Indicators: {len(indicator_columns)}")
            print(f"   Indicator List: {indicator_columns[:5]}..." if len(indicator_columns) > 5 else f"   Indicator List: {indicator_columns}")

            # Display some indicator values
            if 'RSI_14' in data.columns:
                rsi_value = latest['RSI_14']
                print(f"   RSI(14): {rsi_value:.2f}" if not pd.isna(rsi_value) else "   RSI(14): N/A")

            if 'SMA_20' in data.columns:
                sma_value = latest['SMA_20']
                print(f"   SMA(20): ${sma_value:.2f}" if not pd.isna(sma_value) else "   SMA(20): N/A")

            if 'MACD_12_26' in data.columns:
                macd_value = latest['MACD_12_26']
                print(f"   MACD: {macd_value:.4f}" if not pd.isna(macd_value) else "   MACD: N/A")

            return True
        else:
            print("❌ Failed to retrieve K-line data")
            return False

    except Exception as e:
        print(f"❌ DEX K-line data retrieval test failed: {e}")
        return False


async def test_multiple_indicators():
    """Tests multiple indicator configurations"""
    print("\n=== Testing Multiple Indicator Configurations ===")

    test_configs = [
        {
            'name': 'Basic Trend Indicators',
            'config': {
                'sma': {'period': 10},
                'ema': {'period': 21},
                'rsi': {'period': 14}
            }
        },
        {
            'name': 'Advanced Technical Indicators',
            'config': {
                'macd': {'fast': 8, 'slow': 21, 'signal': 5},
                'bb': {'period': 15, 'std': 1.5},
                'stoch': {'k_period': 10, 'd_period': 5}
            }
        },
        {
            'name': 'Volatility Indicators',
            'config': {
                'atr': {'period': 10},
                'bb': {'period': 25, 'std': 2.5}
            }
        }
    ]

    success_count = 0

    for test_case in test_configs:
        try:
            print(f"\nTesting configuration: {test_case['name']}")

            data = await get_klines_with_custom_indicators(
                'binance', 'ETH/USDT', '1h', 30, test_case['config']
            )

            if data is not None and not data.empty:
                indicator_columns = [col for col in data.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
                print(f"   ✅ Successfully calculated {len(indicator_columns)} indicators")
                success_count += 1
            else:
                print(f"   ❌ Configuration failed")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print(f"\nIndicator configuration test results: {success_count}/{len(test_configs)} successful")
    return success_count == len(test_configs)


async def main():
    """Main test function"""
    print("🚀 Starting Crypto PowerData MCP Service Tests")
    print("=" * 50)

    # Import pandas for data processing
    global pd
    import pandas as pd

    test_results = []

    # Test 1: CEX real-time price retrieval
    result1 = await test_cex_price_fetch()
    test_results.append(("CEX Real-time Price Retrieval", result1))

    # Test 2: DEX K-line data retrieval
    result2 = await test_dex_klines_with_indicators()
    test_results.append(("DEX K-line Data Retrieval", result2))

    # Test 3: Multiple indicator configurations
    result3 = await test_multiple_indicators()
    test_results.append(("Multiple Indicator Configurations", result3))

    # Summarize test results
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")

    passed = 0
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1

    print(f"\nOverall result: {passed}/{len(test_results)} tests passed")

    if passed == len(test_results):
        print("🎉 All tests passed! MCP service functionality is normal")
        return True
    else:
        print("⚠️  Some tests failed, please check configuration and network connection")
        return False


if __main__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
