"""
Multi-Platform Marketing Operations & Automated AI Reporting System.
Main Localhost Entry Point.

Inspired by real-world internal automation workflows.
Demonstrates: Python scripting, API ingestion, multi-platform aggregation,
GAS HTML dashboard generation, Claude AI analysis, and Telegram notification.

Usage:
    python main.py
"""

import sys
import os
from pathlib import Path

# Configure UTF-8 for Windows console support
if sys.platform == "win32":
    try:
        if sys.stdout.encoding != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr.encoding != "utf-8":
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.connectors.fb_ads import MetaAdsConnector
from src.connectors.google_ads import GoogleAdsConnector
from src.connectors.google_sheets import GoogleSheetsConnector
from src.core.aggregator import DataAggregator
from src.core.gas_generator import GASDashboardGenerator
from src.ai.claude_analyst import ClaudeAnalyst
from src.notifiers.telegram import TelegramNotifier
from src.config import REPORTS_DIR


def print_banner():
    print("=" * 68)
    print("  MULTI-PLATFORM MARKETING AUTOMATION & AI REPORTING ENGINE")
    print("  Localhost Business Operations Pipeline")
    print("=" * 68)


def run_pipeline():
    print_banner()

    # Step 1: Multi-Platform Data Ingestion
    print("\n[1/5] Ingesting multi-platform marketing data...")
    fb_connector = MetaAdsConnector()
    meta_data = fb_connector.fetch_daily_metrics()
    print(f"      ✓ Meta Ads: {len(meta_data['campaigns'])} active campaigns loaded (Spend: {meta_data['currency']} {meta_data['summary']['total_spend']:,.2f})")

    gad_connector = GoogleAdsConnector()
    google_data = gad_connector.fetch_daily_metrics()
    print(f"      ✓ Google Ads: {len(google_data['campaigns'])} campaigns loaded (Spend: {google_data['currency']} {google_data['summary']['total_spend']:,.2f})")

    sheets_connector = GoogleSheetsConnector()
    sheets_data = sheets_connector.fetch_kpi_targets()
    print(f"      ✓ Google Sheets: Target benchmarks & rules synchronized.")

    # Step 2: Business Logic & Aggregation
    print("\n[2/5] Aggregating metrics & calculating cross-channel KPIs...")
    aggregator = DataAggregator(meta_data, google_data, sheets_data)
    aggregated_data = aggregator.aggregate()
    kpi = aggregated_data["kpi"]
    curr = aggregated_data["currency"]
    targets = aggregated_data["targets_vs_actual"]

    print(f"      → Total Ad Spend:   {curr} {kpi['total_spend']:,.2f}")
    print(f"      → Total Revenue:    {curr} {kpi['total_revenue']:,.2f}")
    print(f"      → Blended ROAS:     {kpi['blended_roas']:.2f}x (Target: {targets['target_roas']:.2f}x [{targets['roas_status']}])")
    print(f"      → Blended CPA:      {curr} {kpi['blended_cpa']:,.2f} | Purchases: {kpi['total_conversions']}")

    # Step 3: Claude AI Analysis
    print("\n[3/5] Invoking Claude AI intelligence engine...")
    analyst = ClaudeAnalyst()
    ai_insights = analyst.analyze_performance(aggregated_data)
    print(f"      ✓ Model: {ai_insights['model']}")
    print(f"      ✓ {len(ai_insights['action_items'])} operational action items generated.")

    # Step 4: Generate GAS HTML Dashboard
    print("\n[4/5] Generating Google Apps Script (GAS) HTML Dashboard...")
    generator = GASDashboardGenerator()
    report_path = generator.generate(aggregated_data, ai_insights)
    print(f"      ✓ Dashboard generated: {report_path.relative_to(BASE_DIR)}")

    # Step 5: Telegram Notification Dispatch
    print("\n[5/5] Formatting and dispatching Telegram executive briefing...")
    notifier = TelegramNotifier()
    message = notifier.format_message(aggregated_data, ai_insights)
    dispatch_res = notifier.dispatch(message)
    print(f"      ✓ Telegram status: {dispatch_res['status'].upper()}")

    print("\n" + "-" * 68)
    print("TELEGRAM DISPATCH PREVIEW:")
    print("-" * 68)
    print(message)
    print("-" * 68)

    print("\n[DONE] Pipeline completed successfully.")
    print(f"       Open dashboard in browser: file:///{report_path.as_posix()}\n")


if __name__ == "__main__":
    run_pipeline()
