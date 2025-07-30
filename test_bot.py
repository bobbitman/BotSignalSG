#!/usr/bin/env python3
"""
Simple test script to verify bot connection and API keys
Run this before starting the main bot
"""

import sys
import os

# Add the ai-signal-bot directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai-signal-bot'))

from config import Config
from coingecko_helper import CoinGeckoHelper
import requests

def test_telegram_connection():
    """Test if Telegram bot token is valid"""
    print("🤖 Testing Telegram Bot Connection...")
    
    try:
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                bot_data = bot_info['result']
                print(f"✅ Bot connected successfully!")
                print(f"   Bot Name: {bot_data.get('first_name')}")
                print(f"   Username: @{bot_data.get('username')}")
                print(f"   Bot ID: {bot_data.get('id')}")
                return True
            else:
                print(f"❌ Telegram API error: {bot_info}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_openai_connection():
    """Test if OpenAI API key is valid"""
    print("\n🧠 Testing OpenAI Connection...")
    
    try:
        import openai
        openai.api_key = Config.OPENAI_API_KEY
        
        # Simple test request
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello from OpenAI!'"}],
            max_tokens=10
        )
        
        if response.choices:
            print("✅ OpenAI connected successfully!")
            print(f"   Response: {response.choices[0].message.content.strip()}")
            return True
        else:
            print("❌ No response from OpenAI")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return False

def test_coingecko_connection():
    """Test CoinGecko API connection"""
    print("\n💰 Testing CoinGecko Connection...")
    
    try:
        cg = CoinGeckoHelper()
        
        # Test with Bitcoin
        result = cg.analyze_ticker('btc')
        
        if result['success']:
            price_data = result['current_price']
            print("✅ CoinGecko connected successfully!")
            print(f"   BTC Price: ${price_data.get('usd', 0):.2f} USD")
            print(f"   24h Change: {price_data.get('usd_24h_change', 0):.2f}%")
            return True
        else:
            print(f"❌ CoinGecko error: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ CoinGecko error: {e}")
        return False

def main():
    """Run all connection tests"""
    print("🚀 BotSignalSGBot Connection Tests\n")
    
    try:
        # Validate config first
        Config.validate_config()
        print("✅ Configuration validation passed!\n")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    # Run tests
    telegram_ok = test_telegram_connection()
    openai_ok = test_openai_connection()
    coingecko_ok = test_coingecko_connection()
    
    print(f"\n📊 Test Results:")
    print(f"   Telegram: {'✅' if telegram_ok else '❌'}")
    print(f"   OpenAI: {'✅' if openai_ok else '❌'}")
    print(f"   CoinGecko: {'✅' if coingecko_ok else '❌'}")
    
    if telegram_ok and openai_ok and coingecko_ok:
        print(f"\n🎉 All tests passed! Your bot is ready to run.")
        print(f"   Start it with: python run_bot.py")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Fix the issues above before running the bot.")
        return False

if __name__ == '__main__':
    main()