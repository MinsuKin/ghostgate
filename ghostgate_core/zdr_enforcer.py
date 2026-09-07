"""
GhostGate Core: Zero Data Retention (ZDR) Enforcer & Policy Engine.
Validates outbound API calls, strips telemetry, and triggers air-gap isolation.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


class ZDREnforcer:
    """
    Enforces strict zero-data retention policies on outbound LLM calls.
    """

    STRIPPED_HEADER_PREFIXES = (
        "x-stainless-",          # Common SDK telemetry
        "x-request-telemetry",
        "x-client-session",
        "x-datadog-",
        "x-newrelic-",
        "sec-ch-ua",
    )

    STRIPPED_HEADERS = {
        "user-agent",           # Strip fingerprinting client details
        "cookie",
        "x-forwarded-for",
        "client-id",
    }

    def __init__(
        self,
        strict_mode: bool = True,
        disallowed_endpoints: Optional[List[str]] = None,
        airgap_triggers: Optional[List[str]] = None,
    ):
        self.strict_mode = strict_mode
        self.disallowed_endpoints = disallowed_endpoints or [
            "/v1/fine_tuning",
            "/v1/audio/transcriptions",
        ]
        self.airgap_triggers = airgap_triggers or [
            "# @airgap",
            "# @top-secret",
            "BEGIN RSA PRIVATE KEY",
            "BEGIN OPENSSH PRIVATE KEY",
            "BEGIN EC PRIVATE KEY",
            "BEGIN PRIVATE KEY",
        ]

    def should_route_to_airgap(self, raw_text_or_json: Any) -> Tuple[bool, Optional[str]]:
        """
        Determines if the payload contains classified tokens that require local air-gap routing.
        """
        content_str = str(raw_text_or_json)
        for trigger in self.airgap_triggers:
            if trigger in content_str:
                return True, trigger
        return False, None

    def validate_endpoint(self, path: str) -> Tuple[bool, Optional[str]]:
        """
        Verifies that the target path does not violate the enterprise ZDR policy.
        """
        for disallowed in self.disallowed_endpoints:
            if disallowed in path:
                return (
                    False,
                    f"Endpoint '{path}' is blocked by GhostGate ZDR policy. "
                    f"(Rule match: '{disallowed}')",
                )
        return True, None

    def sanitize_headers(
        self,
        incoming_headers: Dict[str, str],
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Strips tracking, telemetry, and fingerprinting headers before forwarding to upstream LLMs.
        Injects ZDR audit headers.
        """
        sanitized = {}
        for key, value in incoming_headers.items():
            lower_key = key.lower()
            if lower_key in self.STRIPPED_HEADERS:
                continue
            if any(lower_key.startswith(pfx) for pfx in self.STRIPPED_HEADER_PREFIXES):
                continue
            sanitized[key] = value

        # Set standardized client identity to prevent fingerprinting
        sanitized["user-agent"] = "GhostGate-ZDR-Client/1.0"

        # Inject audit headers
        if custom_headers:
            sanitized.update(custom_headers)

        sanitized["X-GhostGate-ZDR"] = "enforced"
        sanitized["X-GhostGate-Shield"] = "active"

        return sanitized
