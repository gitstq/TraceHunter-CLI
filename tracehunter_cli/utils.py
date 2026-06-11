"""
Color utility for terminal output - Zero dependency ANSI color codes.
"""

class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"

    @staticmethod
    def disable():
        """Disable colors for non-TTY environments."""
        for attr in ["RESET", "BOLD", "DIM", "UNDERLINE",
                      "BLACK", "RED", "GREEN", "YELLOW", "BLUE",
                      "MAGENTA", "CYAN", "WHITE",
                      "BG_RED", "BG_GREEN", "BG_YELLOW", "BG_BLUE"]:
            setattr(Colors, attr, "")

    @staticmethod
    def risk_color(score):
        """Return color based on risk score."""
        if score >= 80:
            return Colors.RED
        elif score >= 60:
            return Colors.YELLOW
        elif score >= 40:
            return Colors.CYAN
        return Colors.GREEN


def print_banner():
    """Print TraceHunter-CLI banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}  ╔══════════════════════════════════════════════════════╗
  ║     TraceHunter-CLI v1.0.0                        ║
  ║     Lightweight Username Digital Footprint Tracker ║
  ║     轻量级用户名数字足迹智能追踪引擎                    ║
  ╚══════════════════════════════════════════════════════╝{Colors.RESET}
    """
    print(banner)


def parse_args():
    """Parse command line arguments - Zero dependency implementation."""
    import argparse
    parser = argparse.ArgumentParser(
        prog="tracehunter",
        description="TraceHunter-CLI - Lightweight Terminal Username Digital Footprint Tracking Engine",
        epilog="Examples:\n"
               "  tracehunter -u johndoe\n"
               "  tracehunter -u johndoe --categories social,tech\n"
               "  tracehunter -u johndoe --output-html report.html\n"
               "  tracehunter -u johndoe --proxy socks5://127.0.0.1:1080\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-u", "--username", type=str, help="Target username to search")
    parser.add_argument("-p", "--proxy", type=str, default=None, help="Proxy URL (http/socks5)")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("-w", "--workers", type=int, default=20, help="Max concurrent workers (default: 20)")
    parser.add_argument("-c", "--categories", type=str, default=None, help="Comma-separated site categories to include")
    parser.add_argument("-e", "--exclude-categories", type=str, default=None, help="Comma-separated site categories to exclude")
    parser.add_argument("--output-json", type=str, default=None, help="Export results to JSON file")
    parser.add_argument("--output-html", type=str, default=None, help="Export results to HTML file")
    parser.add_argument("--list-sites", action="store_true", help="List all available sites and exit")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    return parser.parse_args()
