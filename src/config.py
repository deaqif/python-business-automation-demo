"""
Configuration module for the automation pipeline.
Loads settings from environment variables or sensible localhost defaults.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DIR = DATA_DIR / "sample"
REPORTS_DIR = DATA_DIR / "reports"

# Ensure output directories exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Optional dotenv loader (graceful fallback if python-dotenv is not installed)
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# Application Settings
APP_ENV = os.getenv("APP_ENV", "demo")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Meta Ads API Settings
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "mock_meta_token")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "act_88492019482")

# Google Ads API Settings
GOOGLE_ADS_CLIENT_ID = os.getenv("GOOGLE_ADS_CLIENT_ID", "mock_client_id")
GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "mock_dev_token")

# Google Sheets Settings
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "mock_sheet_id")

# Claude / Anthropic API Settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Telegram Bot Notification Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
