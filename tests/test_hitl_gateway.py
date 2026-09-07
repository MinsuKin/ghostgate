import pytest
from ghostgate_core.hitl_gateway import HITLGateway, ActionRiskLevel
from rawhuman_engine.biomechanics import BiomechanicalAnalyzer, generate_human_like_trajectory


def test_hitl_low_risk_auto_permitted():
    gateway = HITLGateway()
    allowed, msg, meta = gateway.evaluate_tool_call(
        tool_name="read_file",
        arguments={"path": "src/main.py"}
    )
    assert allowed is True
    assert msg == "AUTO_PERMITTED_LOW_RISK"
    assert meta["risk_level"] == ActionRiskLevel.LOW.value


def test_hitl_blocks_synthetic_tool_call():
    gateway = HITLGateway()
    # Autonomous AI agent trying to execute a shell command via SendInput / synthetic flag
    allowed, msg, meta = gateway.evaluate_tool_call(
        tool_name="execute_bash",
        arguments={"command": "rm -rf /tmp/data"},
        simulated_flags=0x01  # Synthetic injection
    )
    assert allowed is False
    assert "E_HITL_BLOCKED" in msg
    assert "synthetic OS event injection" in msg
    assert len(gateway.blocked_event_log) > 0


def test_hitl_touchid_hardware_attestation_bypass():
    gateway = HITLGateway()
    # Physical human approved via TouchID Secure Enclave
    allowed, msg, meta = gateway.evaluate_tool_call(
        tool_name="deploy_production",
        arguments={"target": "aws-prod-us-east-1"},
        hardware_attestation_token="touchid_valid_9f83a8b2"
    )
    assert allowed is True
    assert msg == "VERIFIED_HARDWARE_TOUCHID"
    assert meta["verification_method"] == "HARDWARE_SECURE_ENCLAVE_TOUCHID"


def test_hitl_physical_human_motion_pass():
    analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)
    human_points = generate_human_like_trajectory((10.0, 20.0), (400.0, 300.0), steps=20)
    for p in human_points:
        analyzer.add_point(p.x, p.y, p.timestamp)

    gateway = HITLGateway(analyzer=analyzer)
    allowed, msg, meta = gateway.evaluate_tool_call(
        tool_name="git_push",
        arguments={"branch": "main"},
        simulated_flags=0x00
    )
    assert allowed is True
    assert msg == "VERIFIED_PHYSICAL_HUMAN"
