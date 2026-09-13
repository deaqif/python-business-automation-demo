"""
Telegram Bot Notification Dispatcher.
Formats marketing digest, displays terminal simulation, and supports direct API dispatch.
"""

import urllib.request
import urllib.parse
import json
from typing import Dict, Any
from ..config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:
    """
    Handles formatting and sending executive digests to Telegram channels or chats.
    """

    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID

    def format_message(self, data: Dict[str, Any], ai_insights: Dict[str, Any]) -> str:
        """
        Creates a structured, emoji-rich notification message for Telegram.
        """
        kpi = data["kpi"]
        curr = data["currency"]
        targets = data["targets_vs_actual"]
        date = data.get("reporting_date")

        actions_text = "\n".join([f"  • {item}" for item in ai_insights.get("action_items", [])])

        message = (
            f"📊 *DAILY MARKETING BRIEFING — {date}*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *Total Spend:* {curr} {kpi['total_spend']:,.2f}\n"
            f"💵 *Total Revenue:* {curr} {kpi['total_revenue']:,.2f}\n"
            f"📈 *Blended ROAS:* {kpi['blended_roas']:.2f}x (Target: {targets['target_roas']:.2f}x ✅)\n"
            f"🎯 *Blended CPA:* {curr} {kpi['blended_cpa']:,.2f} | Conversions: {kpi['total_conversions']:,}\n"
            f"🌐 *Channel Share:* Meta {data['channel_shares']['meta']['share_pct']}% | Google {data['channel_shares']['google']['share_pct']}%\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚡ *CLAUDE AI OPERATIONAL ACTIONS:*\n"
            f"{actions_text}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 *GAS Dashboard:* `reports/gas_dashboard.html`\n"
            f"🤖 *Triggered via:* Localhost Python Automation Pipeline"
        )
        return message

    def dispatch(self, message: str) -> Dict[str, Any]:
        """
        Dispatches message to Telegram if credentials are set,
        otherwise simulates the dispatch cleanly for the demonstration flow.
        """
        # If live credentials are provided
        if self.bot_token and self.chat_id and self.bot_token != "your_telegram_bot_token_here":
            try:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                payload = {
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    url, data=data, headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_body = response.read().decode("utf-8")
                    return {"status": "sent", "response": json.loads(res_body)}
            except Exception as e:
                return {"status": "error", "error": str(e)}

        # Default Demonstration / Showcase Mode
        return {
            "status": "simulated",
            "channel": "Telegram Bot",
            "recipient": "Configured Operations Admin Chat",
            "message_length": len(message)
        }
