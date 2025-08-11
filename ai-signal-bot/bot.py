import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

from coingecko_helper import CoinGeckoHelper
from openai_helper import OpenAIHelper
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not Config.DEBUG_MODE else logging.DEBUG
)
logger = logging.getLogger(__name__)

class BotSignalSGBot:
    """Main Telegram Bot class for crypto analysis"""
    
    def __init__(self):
        self.coingecko = CoinGeckoHelper()
        self.openai_helper = OpenAIHelper()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        welcome_message = """
🚀 *Welcome to BotSignalSGBot!*

I'm your AI-powered crypto analysis assistant, designed for Singapore traders! 🇸🇬

*Available Commands:*
• `/analyze <ticker>` - Get AI analysis for any cryptocurrency
• `/help` - Show this help message

*Example Usage:*
• `/analyze btc` - Analyze Bitcoin
• `/analyze arb` - Analyze Arbitrum
• `/analyze sol` - Analyze Solana

Ready to analyze some crypto? Just type `/analyze` followed by any coin ticker! 📈

_Powered by OpenAI & CoinGecko APIs_ 🤖
"""
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_message = """
🤖 *BotSignalSGBot Help*

*Main Command:*
`/analyze <ticker>` - Get comprehensive crypto analysis

*Supported Features:*
• Real-time price data (USD & SGD)
• AI-powered technical analysis
• Support/resistance levels
• Entry/exit strategies
• Risk/reward calculations
• Insights!

*Examples:*
• `/analyze btc`
• `/analyze eth`
• `/analyze arb`
• `/analyze matic`

*Tips:*
• Use common ticker symbols (BTC, ETH, SOL, etc.)
• The bot searches by both symbol and coin name
• Analysis includes 24h price changes and market data

Need help? Just ask! 🚀
"""
        await update.message.reply_text(
            help_message,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /analyze <ticker> command"""
        try:
            # Check if ticker is provided
            if not context.args:
                await update.message.reply_text(
                    "❌ Please provide a ticker symbol!\n\n"
                    "Example: `/analyze btc`\n"
                    "Use `/help` for more information.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            ticker = ' '.join(context.args).strip()
            logger.info(f"Analyzing ticker: {ticker} for user {update.effective_user.id}")
            
            # Send "thinking" message
            thinking_msg = await update.message.reply_text(
                f"🤔 Analyzing {ticker.upper()}... This might take a moment!",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Get coin data from CoinGecko
            coin_analysis = self.coingecko.analyze_ticker(ticker)
            
            if not coin_analysis['success']:
                await thinking_msg.edit_text(
                    f"❌ *Error:* {coin_analysis['error']}\n\n"
                    "Try using a different ticker symbol or check the spelling!\n"
                    "Examples: `btc`, `eth`, `sol`, `arb`",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Get AI analysis
            ai_analysis = self.openai_helper.get_ai_analysis(
                ticker=ticker,
                price_data=coin_analysis['current_price'],
                coin_id=coin_analysis['coin_id']
            )
            
            if not ai_analysis:
                await thinking_msg.edit_text(
                    f"❌ Sorry, I couldn't generate analysis for {ticker.upper()} right now.\n\n"
                    "Please try again in a moment!",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Format and send the response
            formatted_response = self.openai_helper.format_telegram_response(
                ticker=ticker,
                analysis=ai_analysis,
                price_data=coin_analysis['current_price']
            )
            
            await thinking_msg.edit_text(
                formatted_response,
                parse_mode=ParseMode.MARKDOWN
            )
            
            logger.info(f"Successfully provided analysis for {ticker} to user {update.effective_user.id}")
            
        except Exception as e:
            logger.error(f"Error in analyze command: {e}")
            await update.message.reply_text(
                "❌ Oops! Something went wrong while analyzing.\n\n"
                "Please try again in a moment. If the problem persists, "
                "the issue might be with external APIs.",
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown commands"""
        await update.message.reply_text(
            "❓ I don't recognize that command!\n\n"
            "Try:\n"
            "• `/start` - Get started\n"
            "• `/analyze <ticker>` - Analyze a crypto\n"
            "• `/help` - Get help\n\n"
            "Example: `/analyze btc`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    def run(self):
        """Start the bot"""
        try:
            # Validate configuration
            Config.validate_config()
            logger.info("Configuration validated successfully")
            
            # Test bot connection
            logger.info("Testing bot connection...")
            import requests
            test_url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/getMe"
            test_response = requests.get(test_url, timeout=10)
            if test_response.status_code == 200:
                bot_info = test_response.json()
                if bot_info.get('ok'):
                    bot_data = bot_info['result']
                    logger.info(f"Bot connected: @{bot_data.get('username')} ({bot_data.get('first_name')})")
                else:
                    raise Exception(f"Bot connection failed: {bot_info}")
            else:
                raise Exception(f"Bot connection failed: HTTP {test_response.status_code}")
            
            # Create application
            application = (
                Application.builder()
                .token(Config.TELEGRAM_BOT_TOKEN)
                .concurrent_updates(True)
                .build()
            )
            
            # Add command handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("analyze", self.analyze_command))
            
            logger.info(f"🚀 Starting {Config.BOT_USERNAME}...")
            logger.info("Bot is running! Press Ctrl+C to stop.")
            logger.info("Try messaging your bot on Telegram!")
            
            # Start the bot
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

def main():
    """Main function to run the bot"""
    bot = BotSignalSGBot()
    bot.run()

if __name__ == '__main__':
    main()