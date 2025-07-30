import openai
import logging
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class OpenAIHelper:
    """Helper class for OpenAI API interactions"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        self.temperature = Config.OPENAI_TEMPERATURE
    
    def build_analysis_prompt(self, ticker: str, price_data: dict, coin_id: str) -> str:
        """
        Build a comprehensive analysis prompt for the AI
        
        Args:
            ticker: Coin ticker symbol
            price_data: Current price data from CoinGecko
            coin_id: CoinGecko coin ID
            
        Returns:
            Formatted prompt string
        """
        usd_price = price_data.get('usd', 0)
        sgd_price = price_data.get('sgd', 0)
        change_24h = price_data.get('usd_24h_change', 0)
        
        prompt = f"""
Analyze the cryptocurrency {ticker.upper()} for a Singapore-based swing trader.

Current Market Data:
- Coin: {coin_id.replace('-', ' ').title()} ({ticker.upper()})
- Current Price: ${usd_price:.4f} USD (S${sgd_price:.4f} SGD)
- 24h Change: {change_24h:.2f}%

Structure your analysis like this:
🚧 Resistance: $X.XX
📊 Support: $X.XX
⛔ Stop Loss: $X.XX
💰 Risk/Reward: X:X
🧠 Summary: Give a short 1-2 sentence summary including target profit levels with realistic expectations and current market conditions.
"""
        return prompt.strip()
    
    def get_ai_analysis(self, ticker: str, price_data: dict, coin_id: str) -> Optional[str]:
        """
        Get AI analysis for a cryptocurrency
        
        Args:
            ticker: Coin ticker symbol
            price_data: Current price data from CoinGecko
            coin_id: CoinGecko coin ID
            
        Returns:
            AI-generated analysis or None if error
        """
        try:
            prompt = self.build_analysis_prompt(ticker, price_data, coin_id)
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful expert crypto trading assistant based in Singapore. Speak in a slightly Singlish tone, like how locals talk. Keep your replies short, friendly, and a bit cheeky if appropriate. Use terms like ""lah"", ""leh"", ""wait a bit"", ""can consider"", ""not bad"", but do not overdo it."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            analysis = response.choices[0].message.content.strip()
            logger.info(f"Successfully generated AI analysis for {ticker}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating AI analysis for {ticker}: {e}")
            return None
    
    def format_telegram_response(self, ticker: str, analysis: str, price_data: dict) -> str:
        """
        Format the AI analysis for Telegram with proper markdown
        
        Args:
            ticker: Coin ticker symbol
            analysis: AI-generated analysis
            price_data: Current price data
            
        Returns:
            Formatted message for Telegram
        """
        usd_price = price_data.get('usd', 0)
        sgd_price = price_data.get('sgd', 0)
        change_24h = price_data.get('usd_24h_change', 0)
        
        # Determine price change emoji
        change_emoji = "🟢" if change_24h >= 0 else "🔴"
        change_sign = "+" if change_24h >= 0 else ""
        
        header = f"""
🚀 *Crypto Analysis: {ticker.upper()}*

💰 *Current Price:* ${usd_price:.4f} USD (S${sgd_price:.4f} SGD)
{change_emoji} *24h Change:* {change_sign}{change_24h:.2f}%

---

{analysis}

---

⚠️ *Disclaimer:* This analysis is for educational purposes only. Always DYOR (Do Your Own Research) and never invest more than you can afford to lose!

_Powered by @BotSignalSGBot 🤖_
"""
        return header.strip()