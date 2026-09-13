"""
Meta / Facebook Ads Data Connector.
Retrieves campaign performance metrics (Spend, Impressions, Clicks, Conversions, ROAS).
"""

import json
from pathlib import Path
from typing import Dict, Any
from ..config import SAMPLE_DIR


class MetaAdsConnector:
    """
    Connector for Meta (Facebook) Marketing API / MCP interface.
    Demonstrates ingestion and normalization of paid social campaign performance.
    """

    def __init__(self, sample_file: Path = None):
        self.sample_file = sample_file or (SAMPLE_DIR / "fb_ads_data.json")

    def fetch_daily_metrics(self) -> Dict[str, Any]:
        """
        Fetches daily aggregated and campaign-level metrics for Meta Ads.
        Returns normalized dictionary with campaign details and summary totals.
        """
        if not self.sample_file.exists():
            raise FileNotFoundError(f"Meta Ads sample data not found at: {self.sample_file}")

        with open(self.sample_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Calculate platform totals
        campaigns = data.get("campaigns", [])
        total_spend = sum(c.get("spend", 0.0) for c in campaigns)
        total_revenue = sum(c.get("revenue", 0.0) for c in campaigns)
        total_clicks = sum(c.get("clicks", 0) for c in campaigns)
        total_impressions = sum(c.get("impressions", 0) for c in campaigns)
        total_conversions = sum(c.get("conversions", 0) for c in campaigns)

        avg_cpc = round(total_spend / total_clicks, 2) if total_clicks > 0 else 0.0
        avg_roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0.0
        cpa = round(total_spend / total_conversions, 2) if total_conversions > 0 else 0.0

        return {
            "platform": "Meta Ads",
            "account_id": data.get("account_id"),
            "reporting_date": data.get("reporting_date"),
            "currency": data.get("currency", "MYR"),
            "summary": {
                "total_spend": round(total_spend, 2),
                "total_revenue": round(total_revenue, 2),
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "avg_cpc": avg_cpc,
                "avg_roas": avg_roas,
                "cpa": cpa,
            },
            "campaigns": campaigns,
        }
