"""
Marketing Data Aggregator & Business Rule Engine.
Combines data from Meta Ads, Google Ads, and Google Sheets targets into a unified data model.
"""

from typing import Dict, Any, List


class DataAggregator:
    """
    Business logic processor for multi-platform marketing metrics.
    Calculates Blended ROAS, Cross-Channel CPA, and evaluates performance against targets.
    """

    def __init__(self, meta_data: Dict[str, Any], google_data: Dict[str, Any], sheets_data: Dict[str, Any]):
        self.meta = meta_data
        self.google = google_data
        self.sheets = sheets_data

    def aggregate(self) -> Dict[str, Any]:
        """
        Processes and aggregates multi-platform performance metrics.
        Returns a comprehensive executive dictionary.
        """
        meta_summary = self.meta.get("summary", {})
        google_summary = self.google.get("summary", {})
        targets = self.sheets.get("targets", {})
        rules = self.sheets.get("operational_rules", {})

        # Cross-platform sums
        total_spend = round(meta_summary.get("total_spend", 0.0) + google_summary.get("total_spend", 0.0), 2)
        total_revenue = round(meta_summary.get("total_revenue", 0.0) + google_summary.get("total_revenue", 0.0), 2)
        total_clicks = meta_summary.get("total_clicks", 0) + google_summary.get("total_clicks", 0)
        total_impressions = meta_summary.get("total_impressions", 0) + google_summary.get("total_impressions", 0)
        total_conversions = meta_summary.get("total_conversions", 0) + google_summary.get("total_conversions", 0)

        # Cross-platform calculated KPIs
        blended_cpc = round(total_spend / total_clicks, 2) if total_clicks > 0 else 0.0
        blended_roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0.0
        blended_cpa = round(total_spend / total_conversions, 2) if total_conversions > 0 else 0.0

        # Combine all campaigns with normalized fields
        all_campaigns: List[Dict[str, Any]] = []

        for c in self.meta.get("campaigns", []):
            item = dict(c)
            item["platform"] = "Meta Ads"
            all_campaigns.append(item)

        for c in self.google.get("campaigns", []):
            item = dict(c)
            item["platform"] = "Google Ads"
            all_campaigns.append(item)

        # Evaluate performance against operational rules
        scale_threshold = rules.get("scale_if_roas_above", 4.0)
        pause_threshold = rules.get("pause_if_roas_below", 1.5)

        high_performers = []
        underperformers = []

        for camp in all_campaigns:
            roas = camp.get("roas", 0.0)
            if roas >= scale_threshold:
                high_performers.append({
                    "name": camp.get("campaign_name"),
                    "platform": camp.get("platform"),
                    "roas": roas,
                    "spend": camp.get("spend"),
                    "recommendation": "SCALE_BUDGET"
                })
            elif roas <= pause_threshold and camp.get("status") == "ACTIVE":
                underperformers.append({
                    "name": camp.get("campaign_name"),
                    "platform": camp.get("platform"),
                    "roas": roas,
                    "spend": camp.get("spend"),
                    "recommendation": "REVIEW_OR_PAUSE"
                })

        # Target comparison
        target_roas = targets.get("target_blended_roas", 3.50)
        roas_status = "EXCEEDED" if blended_roas >= target_roas else "BELOW_TARGET"
        target_cpa = targets.get("target_cpa_max", 18.00)
        cpa_status = "HEALTHY" if blended_cpa <= target_cpa else "ABOVE_TARGET"

        # Platform spend shares
        meta_spend = meta_summary.get("total_spend", 0.0)
        google_spend = google_summary.get("total_spend", 0.0)
        meta_share_pct = round((meta_spend / total_spend) * 100, 1) if total_spend > 0 else 0.0
        google_share_pct = round((google_spend / total_spend) * 100, 1) if total_spend > 0 else 0.0

        return {
            "reporting_date": self.meta.get("reporting_date"),
            "currency": self.meta.get("currency", "MYR"),
            "kpi": {
                "total_spend": total_spend,
                "total_revenue": total_revenue,
                "blended_roas": blended_roas,
                "blended_cpa": blended_cpa,
                "blended_cpc": blended_cpc,
                "total_conversions": total_conversions,
                "total_clicks": total_clicks,
                "total_impressions": total_impressions,
            },
            "channel_shares": {
                "meta": {"spend": meta_spend, "share_pct": meta_share_pct, "roas": meta_summary.get("avg_roas")},
                "google": {"spend": google_spend, "share_pct": google_share_pct, "roas": google_summary.get("avg_roas")}
            },
            "targets_vs_actual": {
                "target_roas": target_roas,
                "actual_roas": blended_roas,
                "roas_status": roas_status,
                "target_cpa": target_cpa,
                "actual_cpa": blended_cpa,
                "cpa_status": cpa_status,
                "target_daily_revenue": targets.get("target_daily_revenue", 4500.0),
                "actual_revenue": total_revenue
            },
            "rule_triggers": {
                "high_performers": high_performers,
                "underperformers": underperformers
            },
            "campaigns": all_campaigns
        }
