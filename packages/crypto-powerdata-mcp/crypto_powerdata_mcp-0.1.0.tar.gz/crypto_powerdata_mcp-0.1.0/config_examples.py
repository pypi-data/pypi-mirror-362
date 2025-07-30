#!/usr/bin/env python3
"""
Crypto PowerData MCP - Configuration Examples
Demonstrates different configuration methods and usage scenarios
"""

import json
from typing import Dict, Any

# ============================================================================
# Environment Variable Configuration Examples
# ============================================================================

# Base OKX API configuration
BASIC_OKX_CONFIG = {
    "OKX_API_KEY": "your_api_key_here",
    "OKX_SECRET_KEY": "your_secret_key_here",
    "OKX_API_PASSPHRASE": "your_passphrase_here",
    "OKX_PROJECT_ID": "your_project_id_here"
}

# Full configuration (includes all optional parameters)
FULL_CONFIG = {
    # OKX API configuration
    "OKX_API_KEY": "your_api_key_here",
    "OKX_SECRET_KEY": "your_secret_key_here",
    "OKX_API_PASSPHRASE": "your_passphrase_here",
    "OKX_PROJECT_ID": "your_project_id_here",
    "OKX_BASE_URL": "https://web3.okx.com/api/v5/",

    # Performance configuration
    "RATE_LIMIT_REQUESTS_PER_SECOND": "10",
    "TIMEOUT_SECONDS": "30",
    "MAX_RETRIES": "3",
    "RETRY_DELAY": "1.0",

    # Technical indicator configuration
    "DEFAULT_INDICATORS": "sma,ema,rsi,macd,bb,stoch",
    "SMA_PERIODS": "20,50,200",
    "EMA_PERIODS": "12,26,50",
    "RSI_PERIOD": "14",
    "MACD_FAST": "12",
    "MACD_SLOW": "26",
    "MACD_SIGNAL": "9",
    "BB_PERIOD": "20",
    "BB_STD": "2",
    "STOCH_K": "14",
    "STOCH_D": "3"
}

# High performance configuration
HIGH_PERFORMANCE_CONFIG = {
    "OKX_API_KEY": "your_api_key_here",
    "OKX_SECRET_KEY": "your_secret_key_here",
    "OKX_API_PASSPHRASE": "your_passphrase_here",
    "OKX_PROJECT_ID": "your_project_id_here",
    "RATE_LIMIT_REQUESTS_PER_SECOND": "20",  # Higher request frequency
    "TIMEOUT_SECONDS": "60",  # Longer timeout
    "MAX_RETRIES": "5",  # More retries
    "CONNECTION_POOL_SIZE": "20"  # Larger connection pool
}

# Conservative configuration (suitable for limited API quotas)
CONSERVATIVE_CONFIG = {
    "OKX_API_KEY": "your_api_key_here",
    "OKX_SECRET_KEY": "your_secret_key_here",
    "OKX_API_PASSPHRASE": "your_passphrase_here",
    "OKX_PROJECT_ID": "your_project_id_here",
    "RATE_LIMIT_REQUESTS_PER_SECOND": "2",  # Lower request frequency
    "TIMEOUT_SECONDS": "120",  # Longer timeout
    "MAX_RETRIES": "1",  # Fewer retries
    "RETRY_DELAY": "5.0"  # Longer retry delay
}

# ============================================================================
# Technical Indicator Configuration Examples
# ============================================================================

# Basic technical indicator configuration
BASIC_INDICATORS = {
    "sma": {"period": 20},
    "ema": {"period": 50},
    "rsi": {"period": 14}
}

# Advanced technical indicator configuration
ADVANCED_INDICATORS = {
    "macd": {"fast": 12, "slow": 26, "signal": 9},
    "rsi": {"period": 14},
    "bb": {"period": 20, "std": 2},
    "stoch": {"k_period": 14, "d_period": 3},
    "atr": {"period": 14},
    "adx": {"period": 14}
}

# Short-term trading indicator configuration
SHORT_TERM_INDICATORS = {
    "sma": {"period": 10},
    "ema": {"period": 21},
    "rsi": {"period": 7},
    "macd": {"fast": 5, "slow": 13, "signal": 5},
    "bb": {"period": 10, "std": 1.5}
}

# Long-term investment indicator configuration
LONG_TERM_INDICATORS = {
    "sma": {"period": 200},
    "ema": {"period": 100},
    "rsi": {"period": 21},
    "macd": {"fast": 26, "slow": 52, "signal": 18},
    "bb": {"period": 50, "std": 2.5}
}

# Volatility analysis indicator configuration
VOLATILITY_INDICATORS = {
    "bb": {"period": 20, "std": 2},
    "atr": {"period": 14},
    "stoch": {"k_period": 14, "d_period": 3},
    "cci": {"period": 20},
    "willr": {"period": 14}
}

# Trend analysis indicator configuration
TREND_INDICATORS = {
    "sma": {"period": 50},
    "ema": {"period": 200},
    "macd": {"fast": 12, "slow": 26, "signal": 9},
    "adx": {"period": 14}
}

# ============================================================================
# MCP Tool Call Examples
# ============================================================================

# Environment variable configuration tool call example
def get_configure_env_vars_example():
    """Get environment variable configuration tool call example"""
    return {
        "tool": "configure_env_vars",
        "arguments": {
            "env_vars": BASIC_OKX_CONFIG
        }
    }

# CEX price retrieval tool call example
def get_cex_price_examples():
    """Get CEX price retrieval tool call example"""
    return [
        {
            "name": "Basic BTC Price Retrieval",
            "call": {
                "tool": "get_cex_price",
                "arguments": {
                    "exchange": "binance",
                    "symbol": "BTC/USDT"
                }
            }
        },
        {
            "name": "ETH Price Retrieval with Fallback Exchanges",
            "call": {
                "tool": "get_cex_price",
                "arguments": {
                    "exchange": "coinbase",
                    "symbol": "ETH/USD",
                    "fallback_exchanges": ["binance", "kraken"]
                }
            }
        },
        {
            "name": "SOL Price Retrieval with Multiple Fallback Exchanges",
            "call": {
                "tool": "get_cex_price",
                "arguments": {
                    "exchange": "nonexistent_exchange",
                    "symbol": "SOL/USDT",
                    "fallback_exchanges": ["binance", "coinbase", "kucoin", "bybit"]
                }
            }
        }
    ]

# DEX data retrieval tool call example
def get_dex_data_examples():
    """Get DEX data retrieval tool call example"""
    return [
        {
            "name": "USDC Basic Data Retrieval",
            "call": {
                "tool": "get_dex_data_with_indicators",
                "arguments": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "1h",
                    "limit": 100
                }
            }
        },
        {
            "name": "USDC with Basic Indicators",
            "call": {
                "tool": "get_dex_data_with_indicators",
                "arguments": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "1h",
                    "limit": 100,
                    "indicators_config": BASIC_INDICATORS
                }
            }
        },
        {
            "name": "USDC with Advanced Indicators",
            "call": {
                "tool": "get_dex_data_with_indicators",
                "arguments": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "4h",
                    "limit": 200,
                    "indicators_config": ADVANCED_INDICATORS
                }
            }
        },
        {
            "name": "BUSD Data Retrieval on BSC",
            "call": {
                "tool": "get_dex_data_with_indicators",
                "arguments": {
                    "chain_index": "56",
                    "token_address": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
                    "timeframe": "1d",
                    "limit": 50,
                    "indicators_config": TREND_INDICATORS
                }
            }
        },
        {
            "name": "Call with Environment Variables",
            "call": {
                "tool": "get_dex_data_with_indicators",
                "arguments": {
                    "chain_index": "1",
                    "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                    "timeframe": "1h",
                    "limit": 100,
                    "indicators_config": BASIC_INDICATORS,
                    "env_vars": BASIC_OKX_CONFIG
                }
            }
        }
    ]

# ============================================================================
# Usage Scenario Examples
# ============================================================================

def get_trading_scenarios():
    """Get configuration examples for different trading scenarios"""
    return {
        "day_trading": {
            "description": "Day Trading Configuration",
            "timeframe": "15m",
            "limit": 96,  # 24 hours of data
            "indicators": SHORT_TERM_INDICATORS,
            "env_config": HIGH_PERFORMANCE_CONFIG
        },
        "swing_trading": {
            "description": "Swing Trading Configuration",
            "timeframe": "4h",
            "limit": 168,  # 4 weeks of data
            "indicators": ADVANCED_INDICATORS,
            "env_config": FULL_CONFIG
        },
        "long_term_analysis": {
            "description": "Long-term Analysis Configuration",
            "timeframe": "1d",
            "limit": 365,  # 1 year of data
            "indicators": LONG_TERM_INDICATORS,
            "env_config": CONSERVATIVE_CONFIG
        },
        "volatility_analysis": {
            "description": "Volatility Analysis Configuration",
            "timeframe": "1h",
            "limit": 720,  # 30 days of data
            "indicators": VOLATILITY_INDICATORS,
            "env_config": FULL_CONFIG
        }
    }

# ============================================================================
# Common Token Addresses
# ============================================================================

COMMON_TOKENS = {
    "ethereum": {
        "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
        "WBTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
    },
    "bsc": {
        "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
        "USDT": "0x55d398326f99059ff775485246999027b3197955",
        "WBNB": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
        "CAKE": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"
    },
    "polygon": {
        "USDC": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
        "USDT": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
        "WMATIC": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
        "DAI": "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063"
    }
}

# ============================================================================
# Helper Functions
# ============================================================================

def print_examples():
    """Print all configuration examples"""
    print("=" * 60)
    print("🔧 Crypto PowerData MCP - Configuration Examples")
    print("=" * 60)

    print("\n📋 Environment Variable Configuration Examples:")
    print("Basic Configuration:", json.dumps(BASIC_OKX_CONFIG, indent=2))

    print("\n📊 Technical Indicator Configuration Examples:")
    print("Basic Indicators:", json.dumps(BASIC_INDICATORS, indent=2))
    print("Advanced Indicators:", json.dumps(ADVANCED_INDICATORS, indent=2))

    print("\n🔧 MCP Tool Call Examples:")
    print("CEX Price Retrieval:", json.dumps(get_cex_price_examples()[0], indent=2))
    print("DEX Data Retrieval:", json.dumps(get_dex_data_examples()[0], indent=2))

    print("\n🎯 Usage Scenario Examples:")
    scenarios = get_trading_scenarios()
    for name, config in scenarios.items():
        print(f"{name}: {config['description']}")

    print("\n💰 Common Token Addresses:")
    for chain, tokens in COMMON_TOKENS.items():
        print(f"{chain.upper()}:")
        for symbol, address in tokens.items():
            print(f"  {symbol}: {address}")

if __name__ == "__main__":
    print_examples()
