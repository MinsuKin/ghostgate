import json
from pathlib import Path
import pytest
from ghostgate_core.redactor import SecretRedactor, MaskingMode
from rawhuman_engine.biomechanics import BiomechanicalAnalyzer
from rawhuman_engine.detector import SyntheticEventDetector

CORPUS_DIR = Path(__file__).parent / "corpus"


def test_secrets_leakage_corpus():
    corpus_file = CORPUS_DIR / "secrets_leakage_corpus.json"
    with open(corpus_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    total_evaluated = len(cases)
    passed_masking = 0
    passed_rehydration = 0

    for case in cases:
        payload = case["payload"]
        expected_masked = case["expected_masked"]
        is_negative = case.get("is_negative_control", False)

        redacted, ctx = redactor.redact_text(payload)

        if not is_negative:
            # 1. Verify all expected secrets are removed from the egress text
            for secret in expected_masked:
                assert secret not in redacted, f"Failed on case '{case['id']}': secret '{secret}' leaked in redacted output!"

            # 2. Verify format-preserving rehydration recovers the exact prompt
            rehydrated = redactor.rehydrate_text(redacted, ctx)
            assert rehydrated == payload, f"Failed on case '{case['id']}': rehydration did not match original payload!"
            passed_masking += 1
            passed_rehydration += 1
        else:
            # Negative control: harmless strings should not be mutilated
            assert ctx.redaction_count == 0, f"False positive masking on negative control '{case['id']}'"

    print(f"\n[CORPUS AUDIT] Evaluated {total_evaluated} cases: {passed_masking} masked, {passed_rehydration} rehydrated perfectly.")


def test_adversarial_prompts_corpus():
    corpus_file = CORPUS_DIR / "adversarial_prompts_corpus.json"
    with open(corpus_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)

    for case in cases:
        payload = case["payload"]
        sensitive_strings = case["sensitive_strings"]

        redacted, ctx = redactor.redact_text(payload)

        for secret in sensitive_strings:
            assert secret not in redacted, f"Adversarial evasion succeeded on case '{case['id']}'! Secret leaked."

        rehydrated = redactor.rehydrate_text(redacted, ctx)
        assert rehydrated == payload, f"Failed rehydration on adversarial prompt '{case['id']}'"


def test_synthetic_agent_corpus():
    corpus_file = CORPUS_DIR / "synthetic_agent_corpus.json"
    with open(corpus_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    detector = SyntheticEventDetector()

    for case in cases:
        analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)
        for pt in case["points"]:
            analyzer.add_point(pt["x"], pt["y"], pt["timestamp"])

        report = analyzer.analyze()
        os_result = detector.inspect_event_metadata(event_flags=case["os_flag"])

        is_bot = case["is_synthetic"]
        if is_bot:
            # Must be flagged either by OS flag or kinematic dynamics
            assert (os_result.is_synthetic or not report.is_human), (
                f"Synthetic agent '{case['id']}' bypassed detection!"
            )
        else:
            # Organic human trajectory must pass
            assert not os_result.is_synthetic, f"Human trajectory '{case['id']}' falsely flagged by OS hook!"
            assert report.is_human, f"Human trajectory '{case['id']}' falsely rejected by kinematics!"
