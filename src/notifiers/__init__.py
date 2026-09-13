"""
Notifiers Package.
Handles delivery of executive briefings via Telegram Bot and console digest.
"""

from .telegram import TelegramNotifier

__all__ = ["TelegramNotifier"]
