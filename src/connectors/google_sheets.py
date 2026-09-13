"""
Google Sheets Data Connector.
Retrieves KPI targets, budget limits, and operational rules from the central database spreadsheet.
"""

import json
from pathlib import Path
from typing import Dict, Any
from ..config import SAMPLE_DIR


class GoogleSheetsConnector:
    """
    Connector for Google Sheets API.
    Simulates fetching business operations targets and syncing daily aggregated performance logs.
    """

    def __init__(self, sample_file: Path = None):
        self.sample_file = sample_file or (SAMPLE_DIR / "sheets_targets.json")

    def fetch_kpi_targets(self) -> Dict[str, Any]:
        """
        Fetches marketing KPI benchmarks and operational rules.
        """
        if not self.sample_file.exists():
            raise FileNotFoundError(f"Google Sheets target data not found at: {self.sample_file}")

        with open(self.sample_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def sync_daily_summary(self, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates writing the daily aggregated metrics back into Google Sheets.
        Returns sync confirmation payload.
        """
        return {
            "status": "success",
            "spreadsheet": "Q3 2026 Marketing Operations Targets & KPI Database",
            "sheet_name": "Daily_Log_Archive",
            "rows_appended": 1,
            "timestamp": summary_data.get("reporting_date"),
        }
