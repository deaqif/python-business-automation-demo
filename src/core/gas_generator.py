"""
Google Apps Script (GAS) HTML Dashboard Generator.
Generates an executive-ready, modern HTML dashboard report compatible with
GAS HtmlService or local standalone browser preview.
"""

from pathlib import Path
from typing import Dict, Any
from ..config import REPORTS_DIR


class GASDashboardGenerator:
    """
    Renders marketing performance data into a standalone, styled HTML report.
    Compatible with Google Apps Script HtmlService deployment.
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or REPORTS_DIR

    def generate(self, data: Dict[str, Any], ai_insights: Dict[str, Any]) -> Path:
        """
        Generates the HTML dashboard file and returns its path.
        """
        kpi = data["kpi"]
        curr = data["currency"]
        targets = data["targets_vs_actual"]
        channels = data["channel_shares"]
        campaigns = data["campaigns"]
        triggers = data["rule_triggers"]

        # Build campaign rows
        campaign_rows_html = ""
        for c in campaigns:
            status_badge = (
                '<span class="badge active">ACTIVE</span>'
                if c.get("status") == "ACTIVE"
                else '<span class="badge paused">PAUSED</span>'
            )
            roas = c.get("roas", 0.0)
            if roas >= 4.0:
                roas_class = "metric-high"
            elif roas <= 1.5:
                roas_class = "metric-low"
            else:
                roas_class = "metric-mid"

            platform_badge = (
                '<span class="badge meta">Meta</span>'
                if c.get("platform") == "Meta Ads"
                else '<span class="badge google">Google</span>'
            )

            campaign_rows_html += f"""
            <tr>
                <td>{platform_badge} <strong>{c.get('campaign_name')}</strong></td>
                <td>{status_badge}</td>
                <td>{curr} {c.get('spend', 0.0):,.2f}</td>
                <td>{c.get('clicks', 0):,}</td>
                <td>{c.get('conversions', 0):,}</td>
                <td class="{roas_class}"><strong>{roas:.2f}x</strong></td>
                <td>{curr} {c.get('revenue', 0.0):,.2f}</td>
            </tr>
            """

        # Build AI action items HTML
        ai_actions_html = ""
        for action in ai_insights.get("action_items", []):
            ai_actions_html += f"<li>{action}</li>"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketing Operations Dashboard — {data.get('reporting_date')}</title>
    <!-- Modern typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #090b0e;
            --surface: #101318;
            --surface-hover: #151921;
            --border: #232833;
            --text: #f3f5f8;
            --muted: #9ba3af;
            --accent-cyan: #67e8f9;
            --accent-purple: #c4b5fd;
            --success: #34d399;
            --warning: #fbbf24;
            --danger: #f87171;
            --radius: 16px;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
            padding: 36px 24px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 32px;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .header-title h1 {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }}
        .header-title h1 span {{
            color: var(--accent-cyan);
        }}
        .header-title p {{
            color: var(--muted);
            font-size: 14px;
            margin-top: 4px;
        }}
        .header-badge {{
            background: rgba(103, 232, 249, 0.08);
            border: 1px solid rgba(103, 232, 249, 0.3);
            color: var(--accent-cyan);
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            padding: 8px 14px;
            border-radius: 999px;
            font-weight: 600;
        }}
        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            margin-bottom: 32px;
        }}
        .kpi-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 22px;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: #3b4252;
        }}
        .kpi-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
            font-weight: 600;
        }}
        .kpi-value {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 8px 0 4px;
            color: #ffffff;
        }}
        .kpi-subtext {{
            font-size: 12px;
            color: var(--muted);
        }}
        .kpi-subtext.highlight {{
            color: var(--success);
            font-weight: 600;
        }}
        /* Two Column Section */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        @media (max-width: 850px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
        .panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 24px;
        }}
        .panel h2 {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        /* AI Box */
        .ai-panel {{
            background: radial-gradient(circle at top right, rgba(139, 92, 246, 0.12), transparent 50%), var(--surface);
            border: 1px solid #3d3b54;
        }}
        .ai-panel h2 {{
            color: var(--accent-purple);
        }}
        .ai-summary-text {{
            font-size: 14px;
            color: #d1d5db;
            line-height: 1.6;
            margin-bottom: 16px;
        }}
        .ai-actions-list {{
            list-style: none;
        }}
        .ai-actions-list li {{
            position: relative;
            padding-left: 24px;
            font-size: 13px;
            color: #e5e7eb;
            margin-bottom: 10px;
            line-height: 1.5;
        }}
        .ai-actions-list li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--accent-cyan);
            font-weight: bold;
        }}
        /* Channel Progress Bars */
        .channel-row {{
            margin-bottom: 18px;
        }}
        .channel-info {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            margin-bottom: 6px;
        }}
        .channel-info span.name {{
            font-weight: 600;
        }}
        .progress-bar-bg {{
            height: 8px;
            background: #1c212c;
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        .fill-meta {{ background: #1877f2; width: {channels['meta']['share_pct']}%; }}
        .fill-google {{ background: #ea4335; width: {channels['google']['share_pct']}%; }}
        /* Table Styles */
        .table-responsive {{
            overflow-x: auto;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            background: var(--surface);
            margin-bottom: 32px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}
        th {{
            background: #13171e;
            color: var(--muted);
            font-weight: 600;
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.06em;
        }}
        td {{
            padding: 14px 18px;
            border-bottom: 1px solid #1a1f28;
            color: #cbd5e1;
        }}
        tr:hover td {{
            background: var(--surface-hover);
        }}
        .badge {{
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        .badge.active {{ background: rgba(52, 211, 153, 0.15); color: var(--success); }}
        .badge.paused {{ background: rgba(155, 163, 175, 0.15); color: var(--muted); }}
        .badge.meta {{ background: rgba(24, 119, 242, 0.2); color: #60a5fa; }}
        .badge.google {{ background: rgba(234, 67, 53, 0.2); color: #f87171; }}
        .metric-high {{ color: var(--success); }}
        .metric-mid {{ color: #ffffff; }}
        .metric-low {{ color: var(--danger); }}
        /* Footer */
        footer {{
            border-top: 1px solid var(--border);
            padding-top: 20px;
            text-align: center;
            font-size: 12px;
            color: var(--muted);
            line-height: 1.6;
        }}
        footer strong {{
            color: #e2e8f0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div class="header-title">
                <h1>Marketing Operations <span>Dashboard</span></h1>
                <p>Automated Multi-Platform Report (Meta Ads + Google Ads + Google Sheets Database)</p>
            </div>
            <div class="header-badge">
                📅 Date: {data.get('reporting_date')} · Localhost Pipeline
            </div>
        </header>

        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Ad Spend</div>
                <div class="kpi-value">{curr} {kpi['total_spend']:,.2f}</div>
                <div class="kpi-subtext">Meta: {channels['meta']['share_pct']}% | Google: {channels['google']['share_pct']}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">{curr} {kpi['total_revenue']:,.2f}</div>
                <div class="kpi-subtext highlight">Target: {curr} {targets['target_daily_revenue']:,.2f} ({round((kpi['total_revenue']/targets['target_daily_revenue'])*100, 1)}%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Blended ROAS</div>
                <div class="kpi-value" style="color: var(--accent-cyan);">{kpi['blended_roas']:.2f}x</div>
                <div class="kpi-subtext highlight">Target Benchmark: {targets['target_roas']:.2f}x ({targets['roas_status']})</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Blended CPA</div>
                <div class="kpi-value">{curr} {kpi['blended_cpa']:,.2f}</div>
                <div class="kpi-subtext">Max Target: {curr} {targets['target_cpa']:,.2f} ({targets['cpa_status']})</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Conversions</div>
                <div class="kpi-value">{kpi['total_conversions']:,}</div>
                <div class="kpi-subtext">Clicks: {kpi['total_clicks']:,} (Avg CPC {curr} {kpi['blended_cpc']:.2f})</div>
            </div>
        </div>

        <!-- 2 Columns: AI Analyst Insights & Channel Distribution -->
        <div class="grid-2">
            <!-- Claude AI Analyst Box -->
            <div class="panel ai-panel">
                <h2>⚡ Claude AI Operational Briefing</h2>
                <div class="ai-summary-text">
                    {ai_insights.get('summary_text', 'Operational evaluation complete.')}
                </div>
                <h3 style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--accent-purple); margin-bottom: 12px;">
                    Recommended Action Items:
                </h3>
                <ul class="ai-actions-list">
                    {ai_actions_html}
                </ul>
            </div>

            <!-- Channel Share & Targets Panel -->
            <div class="panel">
                <h2>📊 Cross-Platform Allocation</h2>
                
                <div class="channel-row">
                    <div class="channel-info">
                        <span class="name">Meta Ads ({channels['meta']['share_pct']}%)</span>
                        <span>{curr} {channels['meta']['spend']:,.2f} (ROAS: {channels['meta']['roas']}x)</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill fill-meta"></div>
                    </div>
                </div>

                <div class="channel-row">
                    <div class="channel-info">
                        <span class="name">Google Ads ({channels['google']['share_pct']}%)</span>
                        <span>{curr} {channels['google']['spend']:,.2f} (ROAS: {channels['google']['roas']}x)</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill fill-google"></div>
                    </div>
                </div>

                <div style="margin-top: 24px; padding-top: 18px; border-top: 1px solid var(--border); font-size: 12px; color: var(--muted);">
                    <p><strong>Database Sync:</strong> Google Sheets target model verified.</p>
                    <p><strong>Operational Rule Triggers:</strong> {len(triggers.get('high_performers', []))} campaign(s) ready to scale, {len(triggers.get('underperformers', []))} campaign(s) requiring review.</p>
                </div>
            </div>
        </div>

        <!-- Campaign Performance Table -->
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Campaign Name</th>
                        <th>Status</th>
                        <th>Spend</th>
                        <th>Clicks</th>
                        <th>Purchases</th>
                        <th>ROAS</th>
                        <th>Revenue</th>
                    </tr>
                </thead>
                <tbody>
                    {campaign_rows_html}
                </tbody>
            </table>
        </div>

        <!-- Production Context Footer -->
        <footer>
            <p><strong>Production Context:</strong> This public dashboard view is a demonstration implementation inspired by a real-world multi-platform marketing operations and reporting automation workflow. The production implementation and business-specific configuration are private.</p>
            <p style="margin-top: 6px;">Developed by <strong>Malek Saifullizan</strong> — AI Automation & Internal Systems Developer</p>
        </footer>
    </div>
</body>
</html>
"""

        output_file = self.output_dir / "gas_dashboard.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_file
