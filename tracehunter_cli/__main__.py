"""
TraceHunter-CLI - Lightweight Terminal Username Digital Footprint Tracking Engine
轻量级终端用户名数字足迹智能追踪引擎
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracehunter_cli.engine import TraceHunter
from tracehunter_cli.reporter import Reporter
from tracehunter_cli.risk_scorer import RiskScorer
from tracehunter_cli.utils import Colors, print_banner, parse_args

def main():
    """Main entry point for TraceHunter-CLI."""
    args = parse_args()
    print_banner()

    if args.version:
        from tracehunter_cli import __version__
        print(f"TraceHunter-CLI v{__version__}")
        sys.exit(0)

    if args.list_sites:
        from tracehunter_cli.sites_db import get_all_sites
        sites = get_all_sites()
        print(f"\n{Colors.CYAN}Available Sites ({len(sites)} total):{Colors.RESET}\n")
        categories = {}
        for site in sites:
            cat = site.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(site["name"])
        for cat, names in sorted(categories.items()):
            print(f"  {Colors.YELLOW}{cat.upper()}{Colors.RESET}: {', '.join(sorted(names))}")
        print()
        sys.exit(0)

    if not args.username:
        print(f"{Colors.RED}Error: Please provide a username with --username or -u{Colors.RESET}")
        print(f"Usage: tracehunter --username <username> [options]")
        sys.exit(1)

    # Initialize engine
    hunter = TraceHunter(
        username=args.username,
        proxy=args.proxy,
        timeout=args.timeout,
        max_workers=args.workers,
        categories=args.categories,
        exclude_categories=args.exclude_categories,
    )

    # Run search
    print(f"\n{Colors.CYAN}[*] Searching for username: {Colors.BOLD}{args.username}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Scanning sites...{Colors.RESET}\n")

    results = hunter.search()

    # Score risks
    scorer = RiskScorer()
    scored_results = scorer.score_all(results)

    # Generate report
    reporter = Reporter(scored_results, args.username)

    if args.output_json:
        reporter.export_json(args.output_json)
        print(f"{Colors.GREEN}[+] JSON report saved: {args.output_json}{Colors.RESET}")

    if args.output_html:
        reporter.export_html(args.output_html)
        print(f"{Colors.GREEN}[+] HTML report saved: {args.output_html}{Colors.RESET}")

    # Print terminal report
    reporter.print_terminal()

    # Summary
    found = sum(1 for r in scored_results if r.get("found"))
    total = len(scored_results)
    high_risk = sum(1 for r in scored_results if r.get("risk_score", 0) >= 70)

    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}Summary: {Colors.GREEN}{found}{Colors.CYAN}/{total} accounts found", end="")
    if high_risk > 0:
        print(f" | {Colors.RED}{high_risk} high-risk{Colors.CYAN}", end="")
    print(f"{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
