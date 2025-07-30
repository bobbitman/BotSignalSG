#!/usr/bin/env python3
"""
Debug script to check if environment variables are loaded correctly
Run this to troubleshoot .env file issues
"""

import os
from dotenv import load_dotenv

# Try to load .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')

print(f"Current directory: {current_dir}")
print(f"Looking for .env file at: {env_path}")
print(f".env file exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    print(f".env file size: {os.path.getsize(env_path)} bytes")
    print("\n.env file contents:")
    with open(env_path, 'r') as f:
        content = f.read()
        # Don't print actual keys, just show structure
        lines = content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0]
                print(f"  {key}=***")
            elif line.strip():
                print(f"  {line}")

# Load the environment variables
load_dotenv(env_path)

print(f"\nAfter loading .env:")
print(f"TELEGRAM_BOT_TOKEN loaded: {'Yes' if os.getenv('TELEGRAM_BOT_TOKEN') else 'No'}")
print(f"OPENAI_API_KEY loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
print(f"BOT_USERNAME: {os.getenv('BOT_USERNAME', 'Not set')}")
print(f"DEBUG_MODE: {os.getenv('DEBUG_MODE', 'Not set')}")

# Test the config class
try:
    from config import Config
    Config.validate_config()
    print("\n✅ Configuration validation passed!")
except Exception as e:
    print(f"\n❌ Configuration validation failed: {e}")