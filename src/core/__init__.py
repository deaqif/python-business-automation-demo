"""
Core Business Logic Package.
Aggregates cross-channel metrics and generates Google Apps Script (GAS) HTML dashboards.
"""

from .aggregator import DataAggregator
from .gas_generator import GASDashboardGenerator

__all__ = ["DataAggregator", "GASDashboardGenerator"]
