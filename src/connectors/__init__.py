"""
Data Connectors Package
Handles multi-platform data ingestion from Meta Ads, Google Ads, and Google Sheets.
"""

from .fb_ads import MetaAdsConnector
from .google_ads import GoogleAdsConnector
from .google_sheets import GoogleSheetsConnector

__all__ = ["MetaAdsConnector", "GoogleAdsConnector", "GoogleSheetsConnector"]
