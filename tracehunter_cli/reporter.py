"""
Report generator for TraceHunter-CLI.
Supports terminal (colored), JSON, and HTML output formats.
"""

import json
import os
import time
from datetime import datetime, timezone

from tracehunter_cli.utils import Colors
from tracehunter_cli.risk_scorer import RiskScorer


class Reporter:
    """Generate reports in multiple formats."""

    def __init__(self, results, username):
        """Initialize reporter.

        Args:
            results: List of scored search results
            username: Target username
        """
        self.results = results
        self.username = username
        self.scorer = RiskScorer()
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def print_terminal(self):
        """Print colored terminal report."""
        found = [r for r in self.results if r.get("found")]
        overall = self.scorer.get_overall_risk(self.results)

        # Overall risk assessment
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}  DIGITAL FOOTPRINT ASSESSMENT{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"  Username:    {Colors.CYAN}{self.username}{Colors.RESET}")
        print(f"  Scan Time:   {self.timestamp}")
        print(f"  Overall Risk: {Colors.BOLD}{overall['level']}{Colors.RESET} ({overall['overall_score']}/100)")
        print(f"  Accounts:    {Colors.GREEN}{overall['total_accounts']}{Colors.RESET} found")
        print(f"  High Risk:   {Colors.RED}{overall['high_risk_count']}{Colors.RESET}")
        print(f"  {Colors.DIM}{overall['message']}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

        if not found:
            print(f"\n  {Colors.YELLOW}No accounts found for '{self.username}'.{Colors.RESET}")
            return

        # Sort by risk score descending
        found.sort(key=lambda x: x.get("risk_score", 0), reverse=True)

        # Group by category
        categories = {}
        for r in found:
            cat = r.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)

        print(f"\n{Colors.BOLD}  FOUND ACCOUNTS BY CATEGORY{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

        for cat in sorted(categories.keys()):
            accounts = categories[cat]
            print(f"\n  {Colors.YELLOW}{cat.upper()}{Colors.RESET} ({len(accounts)} accounts)")
            print(f"  {'-'*56}")

            for acc in accounts:
                score = acc.get("risk_score", 0)
                level = acc.get("risk_level", "UNKNOWN")
                color = Colors.risk_color(score)
                risk_bar = self._build_risk_bar(score)

                print(f"    {Colors.GREEN}\u2713{Colors.RESET} "
                      f"{acc['name']:<22s} "
                      f"{color}{risk_bar}{Colors.RESET} "
                      f"{color}{level}{Colors.RESET} "
                      f"({score}/100)")

                if acc.get("title"):
                    print(f"      {Colors.DIM}Title: {acc['title'][:60]}{Colors.RESET}")
                if acc.get("description"):
                    print(f"      {Colors.DIM}Desc:  {acc['description'][:60]}{Colors.RESET}")
                print(f"      {Colors.DIM}URL:   {acc['url']}{Colors.RESET}")

        # Recommendations
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}  RECOMMENDATIONS{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

        if overall["overall_score"] >= 60:
            print(f"  {Colors.RED}[!] Consider reviewing privacy settings on high-risk platforms{Colors.RESET}")
            print(f"  {Colors.RED}[!] Remove or restrict personal information from public profiles{Colors.RESET}")
            print(f"  {Colors.RED}[!] Use unique usernames across platforms to reduce correlation{Colors.RESET}")
        elif overall["overall_score"] >= 40:
            print(f"  {Colors.YELLOW}[~] Review accounts with moderate risk scores{Colors.RESET}")
            print(f"  {Colors.YELLOW}[~] Consider using pseudonyms on non-essential platforms{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}[+] Digital footprint appears well-managed{Colors.RESET}")
            print(f"  {Colors.GREEN}[+] Continue using privacy-conscious practices{Colors.RESET}")

        print()

    def _build_risk_bar(self, score):
        """Build a visual risk bar."""
        filled = int(score / 5)
        return f"[{'#' * filled}{'-' * (20 - filled)}]"

    def export_json(self, filepath):
        """Export results to JSON file.

        Args:
            filepath: Output file path
        """
        overall = self.scorer.get_overall_risk(self.results)

        report = {
            "tracehunter_version": "1.0.0",
            "scan_info": {
                "username": self.username,
                "timestamp": self.timestamp,
                "total_sites_scanned": len(self.results),
                "accounts_found": overall["total_accounts"],
            },
            "risk_assessment": overall,
            "accounts": [
                {
                    "name": r["name"],
                    "category": r.get("category", "other"),
                    "url": r.get("url", ""),
                    "found": r.get("found", False),
                    "status": r.get("status", "unknown"),
                    "risk_score": r.get("risk_score", 0),
                    "risk_level": r.get("risk_level", "UNKNOWN"),
                    "title": r.get("title", ""),
                    "description": r.get("description", ""),
                    "response_time": r.get("response_time", 0),
                    "http_code": r.get("http_code", 0),
                    "tags": r.get("tags", []),
                    "error": r.get("error"),
                }
                for r in self.results
            ],
        }

        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def export_html(self, filepath):
        """Export results to HTML report.

        Args:
            filepath: Output file path
        """
        overall = self.scorer.get_overall_risk(self.results)
        found = [r for r in self.results if r.get("found")]
        found.sort(key=lambda x: x.get("risk_score", 0), reverse=True)

        risk_color_map = {
            "CRITICAL": "#dc3545",
            "HIGH": "#ffc107",
            "MEDIUM": "#17a2b8",
            "LOW": "#28a745",
            "MINIMAL": "#28a745",
            "NONE": "#6c757d",
        }

        overall_color = risk_color_map.get(overall["level"], "#6c757d")

        accounts_html = ""
        for acc in found:
            score = acc.get("risk_score", 0)
            level = acc.get("risk_level", "UNKNOWN")
            color = risk_color_map.get(level, "#6c757d")
            pct = min(score, 100)

            accounts_html += f"""
            <div class="account-card" style="border-left: 4px solid {color}">
                <div class="account-header">
                    <span class="account-name">{acc['name']}</span>
                    <span class="risk-badge" style="background: {color}">{level} ({score}/100)</span>
                </div>
                <div class="account-meta">
                    <span class="category">{acc.get('category', 'other')}</span>
                    <span class="response-time">{acc.get('response_time', 0)}s</span>
                </div>
                <div class="risk-bar-container">
                    <div class="risk-bar" style="width: {pct}%; background: {color}"></div>
                </div>
                <div class="account-url">
                    <a href="{acc['url']}" target="_blank">{acc['url']}</a>
                </div>
                {"<div class='account-title'>" + acc.get('title', '') + "</div>" if acc.get('title') else ""}
                {"<div class='account-desc'>" + acc.get('description', '') + "</div>" if acc.get('description') else ""}
            </div>
            """

        not_found_count = sum(1 for r in self.results if r.get("status") == "not_found")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TraceHunter Report - {self.username}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0d1117; color: #c9d1d9; line-height: 1.6;
            max-width: 900px; margin: 0 auto; padding: 20px;
        }}
        .header {{
            text-align: center; padding: 30px 0;
            border-bottom: 1px solid #30363d; margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px; color: #58a6ff; margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #8b949e; font-size: 14px;
        }}
        .overview {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px; margin-bottom: 30px;
        }}
        .stat-card {{
            background: #161b22; border: 1px solid #30363d;
            border-radius: 8px; padding: 20px; text-align: center;
        }}
        .stat-value {{
            font-size: 32px; font-weight: bold; color: #58a6ff;
        }}
        .stat-label {{
            color: #8b949e; font-size: 13px; margin-top: 5px;
        }}
        .risk-overview {{
            background: #161b22; border: 1px solid #30363d;
            border-radius: 8px; padding: 20px; margin-bottom: 30px;
            border-left: 4px solid {overall_color};
        }}
        .risk-overview h2 {{
            color: {overall_color}; margin-bottom: 10px;
        }}
        .risk-overview p {{
            color: #8b949e; font-size: 14px;
        }}
        .section-title {{
            color: #58a6ff; font-size: 18px; margin-bottom: 15px;
            padding-bottom: 10px; border-bottom: 1px solid #30363d;
        }}
        .account-card {{
            background: #161b22; border: 1px solid #30363d;
            border-radius: 8px; padding: 15px; margin-bottom: 10px;
        }}
        .account-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 8px;
        }}
        .account-name {{
            font-weight: bold; font-size: 16px; color: #f0f6fc;
        }}
        .risk-badge {{
            padding: 3px 10px; border-radius: 12px;
            font-size: 12px; font-weight: bold; color: #0d1117;
        }}
        .account-meta {{
            display: flex; gap: 15px; margin-bottom: 8px;
        }}
        .account-meta span {{
            font-size: 12px; color: #8b949e;
            background: #21262d; padding: 2px 8px; border-radius: 4px;
        }}
        .risk-bar-container {{
            height: 6px; background: #21262d; border-radius: 3px;
            margin: 10px 0; overflow: hidden;
        }}
        .risk-bar {{
            height: 100%; border-radius: 3px; transition: width 0.3s;
        }}
        .account-url a {{
            color: #58a6ff; text-decoration: none; font-size: 13px;
        }}
        .account-url a:hover {{ text-decoration: underline; }}
        .account-title, .account-desc {{
            color: #8b949e; font-size: 13px; margin-top: 5px;
            overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
        }}
        .footer {{
            text-align: center; padding: 20px 0; margin-top: 30px;
            border-top: 1px solid #30363d; color: #8b949e; font-size: 13px;
        }}
        .footer a {{ color: #58a6ff; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TraceHunter Report</h1>
        <div class="subtitle">Username Digital Footprint Analysis</div>
    </div>

    <div class="overview">
        <div class="stat-card">
            <div class="stat-value">{overall['total_accounts']}</div>
            <div class="stat-label">Accounts Found</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: {overall_color}">{overall['overall_score']}</div>
            <div class="stat-label">Overall Risk Score</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{overall['high_risk_count']}</div>
            <div class="stat-label">High Risk Accounts</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{not_found_count}</div>
            <div class="stat-label">Not Found</div>
        </div>
    </div>

    <div class="risk-overview">
        <h2>Risk Assessment: {overall['level']}</h2>
        <p>{overall['message']}</p>
    </div>

    <div class="section-title">Found Accounts ({len(found)})</div>
    {accounts_html if found else '<p style="color: #8b949e;">No accounts found.</p>'}

    <div class="footer">
        <p>Generated by <a href="#">TraceHunter-CLI v1.0.0</a> on {self.timestamp}</p>
        <p>For educational and authorized security research purposes only.</p>
    </div>
</body>
</html>"""

        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
