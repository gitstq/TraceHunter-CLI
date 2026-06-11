"""
Core search engine for TraceHunter-CLI.
Multi-threaded username search across curated sites using only Python standard library.
"""

import json
import ssl
import time
import urllib.request
import urllib.error
import urllib.parse
import concurrent.futures
import re
from html.parser import HTMLParser

from tracehunter_cli.sites_db import get_all_sites, get_sites_by_categories, get_sites_excluding_categories


class TitleExtractor(HTMLParser):
    """Extract title and meta description from HTML - zero dependency."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self._in_title = False
        self._in_meta = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            attr_dict = dict(attrs)
            if attr_dict.get("name", "").lower() == "description":
                self.description = attr_dict.get("content", "")

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


class TraceHunter:
    """Core search engine for username digital footprint tracking."""

    def __init__(self, username, proxy=None, timeout=10, max_workers=20,
                 categories=None, exclude_categories=None):
        """Initialize TraceHunter engine.

        Args:
            username: Target username to search for
            proxy: Optional proxy URL (http/socks5)
            timeout: Request timeout in seconds
            max_workers: Maximum concurrent threads
            categories: List of categories to include
            exclude_categories: List of categories to exclude
        """
        self.username = username
        self.proxy = proxy
        self.timeout = timeout
        self.max_workers = max_workers
        self.categories = categories
        self.exclude_categories = exclude_categories
        self.results = []
        self._ssl_context = self._create_ssl_context()
        self._opener = self._create_opener()

    def _create_ssl_context(self):
        """Create SSL context that doesn't verify certificates (for speed)."""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def _create_opener(self):
        """Create URL opener with optional proxy support."""
        handlers = []
        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({
                "http": self.proxy,
                "https": self.proxy,
            })
            handlers.append(proxy_handler)
        if handlers:
            return urllib.request.build_opener(*handlers)
        return urllib.request.build_opener()

    def _build_url(self, site):
        """Build the target URL for a site."""
        check_url = site.get("check_url", site.get("url", ""))
        return check_url.format(username=self.username)

    def _build_profile_url(self, site):
        """Build the profile URL for display."""
        url = site.get("url", "")
        return url.format(username=self.username)

    def _check_site(self, site):
        """Check a single site for the username.

        Returns:
            dict with site info, found status, and extracted data
        """
        result = {
            "name": site["name"],
            "category": site.get("category", "other"),
            "url": self._build_profile_url(site),
            "found": False,
            "status": "unknown",
            "response_time": 0,
            "http_code": 0,
            "title": "",
            "description": "",
            "tags": site.get("tags", []),
            "error": None,
        }

        try:
            url = self._build_url(site)
            start_time = time.time()

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "identity",
                    "Connection": "close",
                }
            )

            response = self._opener.open(req, timeout=self.timeout)
            body = response.read().decode("utf-8", errors="ignore")
            result["http_code"] = response.getcode()
            result["response_time"] = round(time.time() - start_time, 2)

            # Extract title and description
            try:
                parser = TitleExtractor()
                parser.feed(body)
                result["title"] = parser.title.strip()
                result["description"] = parser.description.strip()
            except Exception:
                pass

            # Check presence/absence strings
            presence_strs = site.get("presence_strs", [])
            absence_strs = site.get("absence_strs", [])
            method = site.get("method", "html")

            # Format strings with username
            presence_strs = [s.format(username=self.username) for s in presence_strs]
            absence_strs = [s.format(username=self.username) for s in absence_strs]

            body_lower = body.lower()
            presence_found = any(s.lower() in body_lower for s in presence_strs)
            absence_found = any(s.lower() in body_lower for s in absence_strs)

            if presence_found and not absence_found:
                result["found"] = True
                result["status"] = "found"
            elif absence_found and not presence_found:
                result["found"] = False
                result["status"] = "not_found"
            elif presence_found and absence_found:
                # Ambiguous - lean towards found if more presence strings match
                result["status"] = "ambiguous"
            else:
                result["status"] = "unknown"

        except urllib.error.HTTPError as e:
            result["http_code"] = e.code
            result["response_time"] = round(time.time() - start_time, 2)
            result["error"] = f"HTTP {e.code}"
            if e.code == 404:
                result["found"] = False
                result["status"] = "not_found"
            elif e.code == 200:
                result["status"] = "unknown"
        except urllib.error.URLError as e:
            result["error"] = f"URL Error: {str(e.reason)[:50]}"
            result["response_time"] = round(time.time() - start_time, 2)
        except Exception as e:
            result["error"] = str(e)[:50]
            result["response_time"] = round(time.time() - start_time, 2)

        return result

    def _get_sites(self):
        """Get filtered list of sites to check."""
        sites = get_all_sites()

        if self.categories:
            cats = [c.strip() for c in self.categories.split(",")]
            sites = get_sites_by_categories(cats)

        if self.exclude_categories:
            exc_cats = [c.strip() for c in self.exclude_categories.split(",")]
            sites = get_sites_excluding_categories(exc_cats)

        return sites

    def search(self):
        """Execute search across all sites using thread pool.

        Returns:
            list of result dictionaries
        """
        sites = self._get_sites()
        total = len(sites)
        self.results = []

        print(f"  Scanning {total} sites with {self.max_workers} threads...\n")

        completed = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_site = {executor.submit(self._check_site, site): site for site in sites}

            for future in concurrent.futures.as_completed(future_to_site):
                completed += 1
                try:
                    result = future.result()
                    self.results.append(result)

                    # Progress indicator
                    if result["found"]:
                        print(f"  \u2713 {result['name']:25s} \u2714 FOUND")
                    elif result["status"] == "not_found":
                        print(f"  \u2717 {result['name']:25s} not found")
                    else:
                        print(f"  \u2022 {result['name']:25s} {result['status']}")

                except Exception as e:
                    site = future_to_site[future]
                    self.results.append({
                        "name": site["name"],
                        "category": site.get("category", "other"),
                        "url": self._build_profile_url(site),
                        "found": False,
                        "status": "error",
                        "error": str(e)[:50],
                    })

                # Progress bar
                pct = int(completed / total * 100)
                bar_len = 40
                filled = int(bar_len * completed / total)
                bar = chr(0x2588) * filled + chr(0x2591) * (bar_len - filled)
                print(f"\r  [{bar}] {pct}% ({completed}/{total})", end="", flush=True)
                if completed < total:
                    # Move cursor up to overwrite the status line
                    print(f"\033[A", end="")

        print()  # Final newline after progress bar
        return self.results

    def get_found_accounts(self):
        """Return only found accounts."""
        return [r for r in self.results if r.get("found")]

    def get_stats(self):
        """Return search statistics."""
        total = len(self.results)
        found = sum(1 for r in self.results if r.get("found"))
        not_found = sum(1 for r in self.results if r.get("status") == "not_found")
        errors = sum(1 for r in self.results if r.get("error"))
        avg_time = sum(r.get("response_time", 0) for r in self.results) / max(total, 1)

        return {
            "total": total,
            "found": found,
            "not_found": not_found,
            "errors": errors,
            "avg_response_time": round(avg_time, 2),
            "username": self.username,
        }
