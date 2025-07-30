#!/usr/bin/env python3
"""
Main entry point for BotSignalSGBot
Run this file to start the Telegram bot
"""

import sys
import os

# Add the ai-signal-bot directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai-signal-bot'))

from bot import main

if __name__ == '__main__':
    main()