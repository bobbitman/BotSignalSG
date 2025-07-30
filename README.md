# 🚀 BotSignalSGBot

AI-Powered Crypto Analysis Telegram Bot for Singapore Traders

## 🌟 Features

- **Real-time Crypto Analysis**: Get AI-powered analysis for any cryptocurrency
- **Singapore-focused**: Prices in both USD and SGD, Singlish-flavored responses
- **Technical Analysis**: Support/resistance levels, entry/exit strategies, risk/reward ratios
- **Easy to Use**: Simple `/analyze <ticker>` command interface
- **Comprehensive Data**: Powered by CoinGecko and OpenAI APIs

## 🛠️ Setup Instructions

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd BotSignalSGBot
git checkout BotSignalSGBot  # Switch to your branch
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
COINGECKO_API_KEY=your_coingecko_api_key_here  # Optional
```

### 4. Get Required API Keys

#### Telegram Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Choose a name (e.g., "BotSignalSGBot")
4. Choose a username (e.g., "@BotSignalSGBot")
5. Copy the provided token

#### OpenAI API Key
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key

#### CoinGecko API Key (Optional)
1. Sign up at [CoinGecko](https://www.coingecko.com/en/api)
2. Get your free API key (higher rate limits)

### 5. Run the Bot

```bash
python run_bot.py
```

## 📱 Usage Examples

### Basic Commands

```
/start                 # Welcome message and setup
/help                  # Show help information
/analyze btc           # Analyze Bitcoin
/analyze arb           # Analyze Arbitrum
/analyze sol           # Analyze Solana
```

### Example Analysis Output

```
🚀 Crypto Analysis: BTC

💰 Current Price: $43,250.00 USD (S$58,123.75 SGD)
🟢 24h Change: +2.45%

---

**Support and Resistance Zones**
Key support at $42,000 - this level has been tested multiple times lah. Resistance around $45,000 where we see some selling pressure.

**Entry Strategy** 
Best entry between $42,500-$43,000 on any dip. Wait for volume confirmation before entering your position.

**Stop Loss**
Set stop loss at $41,500 (about 4% risk). This gives you buffer below the support zone.

**Take Profit**
First target: $44,500 (3.5% gain)
Second target: $46,000 (6.5% gain)

**Risk/Reward Ratio**
Looking at 1:2 risk/reward - quite decent for swing trading!

**Market Sentiment**
Overall bullish momentum, but watch out for any macro news that might affect crypto markets.

**Swing Trading Summary**
BTC is showing strength above $42k support with good R:R setup. Entry on dips with tight risk management can work well. Always size your position properly and don't FOMO in!

---

⚠️ Disclaimer: This analysis is for educational purposes only. Always DYOR!

Powered by @BotSignalSGBot 🤖
```

## 🏗️ Architecture

### Project Structure

```
BotSignalSGBot/
├── ai-signal-bot/
│   ├── __init__.py
│   ├── bot.py                 # Main Telegram bot logic
│   ├── coingecko_helper.py    # CoinGecko API integration
│   └── openai_helper.py       # OpenAI API integration
├── config.py                  # Configuration management
├── run_bot.py                # Main entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

### Modular Design

- **`bot.py`**: Handles all Telegram interactions and command routing
- **`coingecko_helper.py`**: Manages cryptocurrency data fetching and ticker validation
- **`openai_helper.py`**: Handles AI prompt generation and response formatting
- **`config.py`**: Centralized configuration management

## 🔮 Future Features (Roadmap)

- [ ] **Chart Integration**: Generate and send price charts
- [ ] **Advanced TA**: Moving averages, RSI, MACD indicators
- [ ] **Portfolio Tracking**: Track multiple positions
- [ ] **Price Alerts**: Set custom price notifications
- [ ] **Historical Analysis**: Analyze past performance
- [ ] **Multi-timeframe Analysis**: 1H, 4H, 1D, 1W views
- [ ] **Sentiment Analysis**: Social media sentiment integration
- [ ] **Risk Management**: Position sizing calculators

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**: Check if your Telegram token is correct
2. **OpenAI errors**: Verify your API key and account credits
3. **Coin not found**: Try different ticker formats (BTC vs Bitcoin)
4. **Rate limiting**: CoinGecko free tier has limits, consider API key

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG_MODE=True
```

This will show detailed logging information.

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ⚠️ Disclaimer

This bot provides educational analysis only. Always do your own research (DYOR) and never invest more than you can afford to lose. Cryptocurrency trading involves significant risk.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ for the Singapore crypto community 🇸🇬