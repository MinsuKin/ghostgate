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


def test_streaming_chunk_boundary_rehydration():
    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    raw_text = "Deploy using AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE and DB=postgres://admin:pw123@db:5432/app"
    redacted_text, ctx = redactor.redact_text(raw_text)

    # Verify that secrets were masked
    assert "AKIAIOSFODNN7EXAMPLE" not in redacted_text
    assert "postgres://admin:pw123@db:5432/app" not in redacted_text

    mock_aws_token = ctx.secret_to_token["AKIAIOSFODNN7EXAMPLE"]
    mock_db_token = ctx.secret_to_token["postgres://admin:pw123@db:5432/app"]

    # Scenario 1: AWS token split across exactly 2 chunks
    split_idx = len("Deploy using AWS_ACCESS_KEY_ID=") + 8  # cuts halfway through mock_aws_token
    chunk_1 = redacted_text[:split_idx]
    chunk_2 = redacted_text[split_idx:]

    emitted = []
    buf = chunk_1
    text1, buf = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=False)
    if text1:
        emitted.append(text1)

    buf += chunk_2
    text2, buf = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=False)
    if text2:
        emitted.append(text2)

    if buf:
        text_final, _ = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=True)
        if text_final:
            emitted.append(text_final)

    reconstructed = "".join(emitted)
    assert reconstructed == raw_text, f"2-chunk split failed! Got: {reconstructed}"

    # Scenario 2: Torture test - 1-byte streaming chunks (worst-case fragmentation)
    emitted_single_char = []
    buf = ""
    for char in redacted_text:
        buf += char
        out, buf = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=False)
        if out:
            emitted_single_char.append(out)

    if buf:
        final_out, _ = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=True)
        if final_out:
            emitted_single_char.append(final_out)

    reconstructed_single = "".join(emitted_single_char)
    assert reconstructed_single == raw_text, f"1-byte stream torture test failed! Got: {reconstructed_single}"

    # Scenario 3: Partial prefix that is NOT a real token
    # e.g. text ending in 'AKIA' followed by non-token 'XYZ'
    false_prefix_text = "Check this model AKIAXYZ test"
    buf = "Check this model AKIA"
    out1, buf = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=False)
    buf += "XYZ test"
    out2, buf = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=False)
    final_out, _ = redactor.rehydrate_streaming_chunk(buf, ctx, is_final=True)
    all_out = out1 + out2 + final_out
    assert all_out == false_prefix_text

