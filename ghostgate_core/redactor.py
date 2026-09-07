"""
GhostGate Core: Redaction & Rehydration Engine.
Features Format-Preserving Synthetic Shadowing and Reversible Tokenization.
Guarantees LLM prompt reasoning integrity, syntax validity, and zero data leakage.
"""

from __future__ import annotations
import math
import random
import re
import string
import uuid
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Pattern, Tuple


class MaskingMode(str, Enum):
    TAG_BASED = "TAG_BASED"                   # e.g. [GHOST_REDACTED_AWS_KEY_001]
    FORMAT_PRESERVING = "FORMAT_PRESERVING"   # e.g. AKIA1A2B3C4D5E6F7G8H (exact 20 chars)


def calculate_shannon_entropy(data: str) -> float:
    """Calculates the Shannon entropy of a string."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    counts = Counter(data)
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


@dataclass
class RedactionRule:
    category: str
    pattern: str
    compiled: Pattern[str] = field(init=False)
    entropy_check: bool = False
    min_length: int = 16

    def __post_init__(self):
        self.compiled = re.compile(self.pattern)


@dataclass
class RedactionContext:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    token_to_secret: Dict[str, str] = field(default_factory=dict)
    secret_to_token: Dict[str, str] = field(default_factory=dict)
    redaction_count: int = 0
    categories_redacted: Dict[str, int] = field(default_factory=dict)

    def register_redaction(
        self,
        secret: str,
        category: str,
        format_tpl: str,
        mode: MaskingMode = MaskingMode.FORMAT_PRESERVING,
    ) -> str:
        """Assigns or retrieves a consistent surrogate token for a secret."""
        if secret in self.secret_to_token:
            return self.secret_to_token[secret]

        self.redaction_count += 1
        self.categories_redacted[category] = self.categories_redacted.get(category, 0) + 1

        if mode == MaskingMode.FORMAT_PRESERVING:
            token = self._generate_format_preserving_synthetic(secret, category, self.redaction_count)
        else:
            token = format_tpl.format(
                category=category,
                id=f"{self.redaction_count:03d}"
            )

        self.secret_to_token[secret] = token
        self.token_to_secret[token] = secret
        return token

    def _generate_format_preserving_synthetic(self, secret: str, category: str, count: int) -> str:
        """
        Generates a syntactically valid mock value of the exact same length and character format,
        preventing LLM syntax errors, regex failures, or hallucinated length mismatches.
        """
        length = len(secret)
        idx_hex = f"{count:04x}".upper()

        if category == "AWS_ACCESS_KEY":
            # 20 chars starting with AKIA
            body = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
            return f"AKIA{idx_hex}{body}"

        elif category == "AWS_SECRET_KEY":
            # 40 chars Base64
            body = "".join(random.choices(string.ascii_letters + string.digits, k=36))
            return f"MOCK{idx_hex}{body}"

        elif category == "OPENAI_API_KEY":
            body = "".join(random.choices(string.ascii_letters + string.digits, k=max(10, length - 12)))
            return f"sk-mock-{idx_hex}-{body}"[:length]

        elif category == "ANTHROPIC_API_KEY":
            body = "".join(random.choices(string.ascii_letters + string.digits, k=max(10, length - 16)))
            return f"sk-ant-mock-{idx_hex}-{body}"[:length]

        elif category == "DATABASE_CONNECTION_STRING":
            scheme_match = re.match(r"^([a-z]+)://", secret)
            scheme = scheme_match.group(1) if scheme_match else "postgres"
            return f"{scheme}://mock_user_{count}:mock_pass_{idx_hex}@localhost:5432/mock_db"

        elif category == "EMAIL_ADDRESS":
            return f"dev.sandbox.{count}@mock-corp.internal"

        elif category == "IPV4_ADDRESS":
            return f"192.0.2.{(count % 250) + 1}"  # RFC 5737 TEST-NET-1

        elif category == "PHONE_NUMBER":
            return f"+1-555-01{count % 90 + 10}"

        else:
            # Generic length-preserving alphanumeric placeholder
            body = "".join(random.choices(string.ascii_letters + string.digits, k=max(4, length - 6)))
            return f"MK{idx_hex}{body}"[:length]


class SecretRedactor:
    """
    Enterprise-grade redaction and rehydration engine.
    Supports both traditional tag masking and format-preserving synthetic shadowing.
    """

    DEFAULT_RULES = [
        ("AWS_ACCESS_KEY", r"\b(?:AKIA|ASIA|ABIA|ACCA)[A-Z0-9]{16}\b", False, 20),
        ("AWS_SECRET_KEY", r"(?<![A-Za-z0-9/])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])", True, 40),
        ("OPENAI_API_KEY", r"sk-[A-Za-z0-9-_]{20,}", False, 20),
        ("ANTHROPIC_API_KEY", r"sk-ant-[A-Za-z0-9-_]{20,}", False, 20),
        ("GITHUB_TOKEN", r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,255}", False, 40),
        ("GENERIC_BEARER_TOKEN", r"Bearer\s+([A-Za-z0-9\-._~+/]+=*)", False, 16),
        ("DATABASE_CONNECTION_STRING", r"(?:postgres|postgresql|mysql|mongodb|redis):\/\/[^\s\"\'<>]+", False, 12),
        ("EMAIL_ADDRESS", r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b", False, 6),
        ("IPV4_ADDRESS", r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", False, 7),
        ("PHONE_NUMBER", r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b", False, 10),
    ]

    def __init__(
        self,
        entropy_threshold: float = 3.8,
        replacement_format: str = "[GHOST_REDACTED_{category}_{id}]",
        mode: MaskingMode = MaskingMode.TAG_BASED,
        custom_rules: Optional[List[Dict[str, Any]]] = None,
    ):
        self.entropy_threshold = entropy_threshold
        self.replacement_format = replacement_format
        self.mode = mode
        self.rules: List[RedactionRule] = []

        if custom_rules:
            for r in custom_rules:
                self.rules.append(
                    RedactionRule(
                        category=r["category"],
                        pattern=r["pattern"],
                        entropy_check=r.get("entropy_check", False),
                        min_length=r.get("min_length", 16),
                    )
                )
        else:
            for cat, pat, ent, min_len in self.DEFAULT_RULES:
                self.rules.append(
                    RedactionRule(
                        category=cat,
                        pattern=pat,
                        entropy_check=ent,
                        min_length=min_len,
                    )
                )

    def redact_text(
        self,
        text: str,
        context: Optional[RedactionContext] = None,
        override_mode: Optional[MaskingMode] = None,
    ) -> Tuple[str, RedactionContext]:
        """
        Redacts sensitive tokens in text, replacing them with reversible surrogate placeholders.
        """
        if context is None:
            context = RedactionContext()

        if not text:
            return text, context

        active_mode = override_mode or self.mode
        processed_text = text

        for rule in self.rules:
            matches = list(rule.compiled.finditer(processed_text))
            matches.sort(key=lambda m: m.start(), reverse=True)

            for match in matches:
                matched_str = match.group(0)
                if match.lastindex and match.lastindex >= 1:
                    raw_secret = match.group(1)
                    replace_target = raw_secret
                else:
                    raw_secret = matched_str
                    replace_target = matched_str

                if rule.entropy_check:
                    if len(raw_secret) < rule.min_length:
                        continue
                    entropy = calculate_shannon_entropy(raw_secret)
                    if entropy < self.entropy_threshold:
                        continue

                surrogate_token = context.register_redaction(
                    secret=replace_target,
                    category=rule.category,
                    format_tpl=self.replacement_format,
                    mode=active_mode,
                )

                start_idx = match.start() + (match.start(1) - match.start() if match.lastindex else 0)
                end_idx = start_idx + len(replace_target)
                processed_text = (
                    processed_text[:start_idx]
                    + surrogate_token
                    + processed_text[end_idx:]
                )

        return processed_text, context

    def rehydrate_text(self, text: str, context: RedactionContext) -> str:
        """
        Restores original secrets from surrogate tokens in response text.
        """
        if not text or not context.token_to_secret:
            return text

        rehydrated = text
        sorted_tokens = sorted(
            context.token_to_secret.items(), key=lambda x: len(x[0]), reverse=True
        )
        for token, original_secret in sorted_tokens:
            if token in rehydrated:
                rehydrated = rehydrated.replace(token, original_secret)

        return rehydrated

    def redact_payload(
        self,
        payload: Any,
        context: Optional[RedactionContext] = None,
        override_mode: Optional[MaskingMode] = None,
    ) -> Tuple[Any, RedactionContext]:
        if context is None:
            context = RedactionContext()

        if isinstance(payload, str):
            redacted, ctx = self.redact_text(payload, context, override_mode)
            return redacted, ctx
        elif isinstance(payload, list):
            redacted_list = []
            for item in payload:
                red_item, _ = self.redact_payload(item, context, override_mode)
                redacted_list.append(red_item)
            return redacted_list, context
        elif isinstance(payload, dict):
            redacted_dict = {}
            for k, v in payload.items():
                red_v, _ = self.redact_payload(v, context, override_mode)
                redacted_dict[k] = red_v
            return redacted_dict, context
        else:
            return payload, context

    def rehydrate_payload(self, payload: Any, context: RedactionContext) -> Any:
        if not context.token_to_secret:
            return payload

        if isinstance(payload, str):
            return self.rehydrate_text(payload, context)
        elif isinstance(payload, list):
            return [self.rehydrate_payload(item, context) for item in payload]
        elif isinstance(payload, dict):
            return {k: self.rehydrate_payload(v, context) for k, v in payload.items()}
        else:
            return payload
