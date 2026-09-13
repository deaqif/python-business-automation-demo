"""
Automated Test Suite for Multi-Platform Marketing Operations Demo.
Tests data connectors, aggregator calculations, GAS HTML generator, and Claude AI module.
Compatible with standard Python unittest and pytest.
"""

import unittest
from pathlib import Path
from src.connectors.fb_ads import MetaAdsConnector
from src.connectors.google_ads import GoogleAdsConnector
from src.connectors.google_sheets import GoogleSheetsConnector
from src.core.aggregator import DataAggregator
from src.core.gas_generator import GASDashboardGenerator
from src.ai.claude_analyst import ClaudeAnalyst
from src.notifiers.telegram import TelegramNotifier


class TestAutomationPipeline(unittest.TestCase):

    def setUp(self):
        self.fb_conn = MetaAdsConnector()
        self.gad_conn = GoogleAdsConnector()
        self.sheets_conn = GoogleSheetsConnector()

    def test_connectors_data_structure(self):
        """Test that all three data connectors return valid payloads."""
        meta = self.fb_conn.fetch_daily_metrics()
        self.assertEqual(meta["platform"], "Meta Ads")
        self.assertGreater(meta["summary"]["total_spend"], 0)

        google = self.gad_conn.fetch_daily_metrics()
        self.assertEqual(google["platform"], "Google Ads")
        self.assertGreater(google["summary"]["total_spend"], 0)

        sheets = self.sheets_conn.fetch_kpi_targets()
        self.assertIn("targets", sheets)
        self.assertIn("target_blended_roas", sheets["targets"])

    def test_aggregator_calculations(self):
        """Test business logic calculations (Blended ROAS, CPA, Revenue)."""
        meta = self.fb_conn.fetch_daily_metrics()
        google = self.gad_conn.fetch_daily_metrics()
        sheets = self.sheets_conn.fetch_kpi_targets()

        aggregator = DataAggregator(meta, google, sheets)
        result = aggregator.aggregate()

        kpi = result["kpi"]
        expected_spend = round(meta["summary"]["total_spend"] + google["summary"]["total_spend"], 2)
        expected_rev = round(meta["summary"]["total_revenue"] + google["summary"]["total_revenue"], 2)

        self.assertEqual(kpi["total_spend"], expected_spend)
        self.assertEqual(kpi["total_revenue"], expected_rev)
        self.assertAlmostEqual(kpi["blended_roas"], round(expected_rev / expected_spend, 2), places=2)

    def test_claude_analyst(self):
        """Test AI analysis and action items generation."""
        meta = self.fb_conn.fetch_daily_metrics()
        google = self.gad_conn.fetch_daily_metrics()
        sheets = self.sheets_conn.fetch_kpi_targets()

        aggregator = DataAggregator(meta, google, sheets)
        result = aggregator.aggregate()

        analyst = ClaudeAnalyst()
        insights = analyst.analyze_performance(result)

        self.assertIn("action_items", insights)
        self.assertGreaterEqual(len(insights["action_items"]), 2)
        self.assertTrue(any("Scale Budget" in item for item in insights["action_items"]))

    def test_gas_dashboard_generation(self):
        """Test that HTML dashboard is properly generated and non-empty."""
        meta = self.fb_conn.fetch_daily_metrics()
        google = self.gad_conn.fetch_daily_metrics()
        sheets = self.sheets_conn.fetch_kpi_targets()

        aggregator = DataAggregator(meta, google, sheets)
        result = aggregator.aggregate()

        analyst = ClaudeAnalyst()
        insights = analyst.analyze_performance(result)

        generator = GASDashboardGenerator()
        html_file = generator.generate(result, insights)

        self.assertTrue(html_file.exists())
        content = html_file.read_text(encoding="utf-8")
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn("Marketing Operations", content)
        self.assertIn("Production Context", content)

    def test_telegram_message_formatting(self):
        """Test Telegram digest formatting."""
        meta = self.fb_conn.fetch_daily_metrics()
        google = self.gad_conn.fetch_daily_metrics()
        sheets = self.sheets_conn.fetch_kpi_targets()

        aggregator = DataAggregator(meta, google, sheets)
        result = aggregator.aggregate()

        analyst = ClaudeAnalyst()
        insights = analyst.analyze_performance(result)

        notifier = TelegramNotifier()
        msg = notifier.format_message(result, insights)

        self.assertIn("DAILY MARKETING BRIEFING", msg)
        self.assertIn("Blended ROAS", msg)
        self.assertIn("CLAUDE AI", msg)


if __name__ == "__main__":
    unittest.main()
