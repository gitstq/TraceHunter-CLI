"""
Risk scoring engine for TraceHunter-CLI.
Evaluates information exposure risk based on discovered accounts.
"""

from tracehunter_cli.utils import Colors


class RiskScorer:
    """Assess information leakage risk based on discovered accounts."""

    # Risk weights by category
    CATEGORY_RISK_WEIGHTS = {
        "social": 0.7,       # Social media - high personal info exposure
        "tech": 0.3,         # Tech platforms - moderate risk
        "media": 0.4,        # Content platforms - moderate risk
        "gaming": 0.5,       # Gaming - moderate risk (often linked to real identity)
        "finance": 0.9,      # Financial - very high risk
        "education": 0.4,    # Education - moderate risk
        "forum": 0.6,        # Forums - moderate-high risk
        "shopping": 0.5,     # Shopping - moderate risk
        "other": 0.3,        # Other - low-moderate risk
    }

    # High-risk tags that increase score
    HIGH_RISK_TAGS = {
        "popular": 0.1,
        "professional": 0.15,
        "business": 0.15,
        "financial": 0.2,
        "identity": 0.15,
        "encrypted": 0.05,
        "security": 0.1,
    }

    # Title-based risk indicators
    TITLE_RISK_KEYWORDS = [
        ("real name", 0.15),
        ("email", 0.2),
        ("phone", 0.25),
        ("address", 0.25),
        ("location", 0.1),
        ("birthday", 0.2),
        ("bio", 0.05),
        ("about", 0.05),
        ("resume", 0.15),
        ("cv", 0.15),
        ("portfolio", 0.1),
        ("hire", 0.1),
        ("contact", 0.1),
    ]

    def score_account(self, result):
        """Calculate risk score for a single account.

        Args:
            result: Search result dictionary

        Returns:
            int: Risk score 0-100
        """
        if not result.get("found"):
            return 0

        score = 0
        category = result.get("category", "other")
        tags = result.get("tags", [])
        title = result.get("title", "").lower()
        description = result.get("description", "").lower()

        # Base score from category
        base = self.CATEGORY_RISK_WEIGHTS.get(category, 0.3) * 40
        score += base

        # Tag-based adjustments
        for tag in tags:
            score += self.HIGH_RISK_TAGS.get(tag, 0) * 100

        # Title/description keyword analysis
        text = f"{title} {description}"
        for keyword, weight in self.TITLE_RISK_KEYWORDS:
            if keyword in text:
                score += weight * 100

        # Has title (more info exposed)
        if result.get("title"):
            score += 5

        # Has description (more info exposed)
        if result.get("description"):
            score += 8

        # Cap at 100
        return min(int(score), 100)

    def get_risk_level(self, score):
        """Get human-readable risk level.

        Args:
            score: Risk score 0-100

        Returns:
            tuple: (level_name, color, emoji)
        """
        if score >= 80:
            return ("CRITICAL", Colors.RED, "DANGER")
        elif score >= 60:
            return ("HIGH", Colors.YELLOW, "WARNING")
        elif score >= 40:
            return ("MEDIUM", Colors.CYAN, "CAUTION")
        elif score >= 20:
            return ("LOW", Colors.GREEN, "INFO")
        else:
            return ("MINIMAL", Colors.GREEN, "OK")

    def score_all(self, results):
        """Score all results and add risk information.

        Args:
            results: List of search result dictionaries

        Returns:
            list: Results with risk_score, risk_level, risk_color added
        """
        scored = []
        for result in results:
            score = self.score_account(result)
            level, color, label = self.get_risk_level(score)
            result["risk_score"] = score
            result["risk_level"] = level
            result["risk_color"] = color
            result["risk_label"] = label
            scored.append(result)
        return scored

    def get_overall_risk(self, results):
        """Calculate overall risk assessment.

        Args:
            results: List of scored results

        Returns:
            dict: Overall risk assessment
        """
        found = [r for r in results if r.get("found")]
        if not found:
            return {
                "overall_score": 0,
                "level": "NONE",
                "message": "No accounts found. Digital footprint appears minimal.",
            }

        scores = [r.get("risk_score", 0) for r in found]
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        total_accounts = len(found)

        # Weight by number of found accounts
        exposure_factor = min(total_accounts / 10, 1.0) * 20
        overall = min(int(avg_score * 0.6 + max_score * 0.2 + exposure_factor), 100)

        level, _, _ = self.get_risk_level(overall)

        if overall >= 80:
            message = f"High digital exposure detected! {total_accounts} accounts found with significant personal information."
        elif overall >= 60:
            message = f"Moderate-high digital exposure. {total_accounts} accounts found, some with sensitive data."
        elif overall >= 40:
            message = f"Moderate digital footprint. {total_accounts} accounts found with some personal data."
        elif overall >= 20:
            message = f"Low digital footprint. {total_accounts} accounts found with minimal exposure."
        else:
            message = f"Minimal digital footprint. Only {total_accounts} accounts found."

        return {
            "overall_score": overall,
            "level": level,
            "message": message,
            "total_accounts": total_accounts,
            "avg_score": round(avg_score),
            "max_score": max_score,
            "high_risk_count": sum(1 for s in scores if s >= 60),
        }
