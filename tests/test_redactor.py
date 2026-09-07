import pytest
from ghostgate_core.redactor import (
    SecretRedactor,
    calculate_shannon_entropy,
    RedactionContext,
    MaskingMode,
)


def test_shannon_entropy():
    assert calculate_shannon_entropy("AAAAAAAAAAAA") == 0.0
    high_ent = calculate_shannon_entropy("wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
    assert high_ent > 4.0


def test_tag_based_redaction_and_rehydration():
    redactor = SecretRedactor(mode=MaskingMode.TAG_BASED)
    raw_prompt = (
        "Please debug this AWS connection:\n"
        "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n"
        "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n"
        "Connecting to database postgres://admin:SuperSecretPass123@db.internal.corp:5432/finance"
    )

    redacted, ctx = redactor.redact_text(raw_prompt)

    assert "AKIAIOSFODNN7EXAMPLE" not in redacted
    assert "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" not in redacted
    assert "[GHOST_REDACTED_" in redacted

    rehydrated = redactor.rehydrate_text(redacted, ctx)
    assert rehydrated == raw_prompt


def test_format_preserving_synthetic_shadowing():
    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    raw_prompt = (
        "Validate this key length:\n"
        "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n"
        "Contact email: security.team@my-enterprise.com\n"
        "DB: postgres://admin:Pass123@prod-cluster.internal:5432/orders"
    )

    redacted, ctx = redactor.redact_text(raw_prompt)

    # 1. Real secrets must not appear
    assert "AKIAIOSFODNN7EXAMPLE" not in redacted
    assert "security.team@my-enterprise.com" not in redacted
    assert "prod-cluster.internal" not in redacted

    # 2. No ugly brackets that confuse LLMs
    assert "[GHOST_REDACTED_" not in redacted

    # 3. Exact format and length preservation for AWS key (20 chars, starting with AKIA)
    masked_key = ctx.secret_to_token["AKIAIOSFODNN7EXAMPLE"]
    assert len(masked_key) == 20
    assert masked_key.startswith("AKIA")

    # 4. Rehydration parity
    rehydrated = redactor.rehydrate_text(redacted, ctx)
    assert rehydrated == raw_prompt


def test_payload_recursive_redaction():
    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": "Contact minsu.security@internal-corp.io or call +1-415-555-0199 for token sk-proj-948192849182391283912"
            }
        ],
        "temperature": 0.2
    }

    redacted_json, ctx = redactor.redact_payload(payload)
    user_content = redacted_json["messages"][0]["content"]

    assert "minsu.security@internal-corp.io" not in user_content
    assert "sk-proj-948192849182391283912" not in user_content

    rehydrated_json = redactor.rehydrate_payload(redacted_json, ctx)
    assert rehydrated_json == payload
