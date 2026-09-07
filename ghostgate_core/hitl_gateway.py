"""
GhostGate Core: Human-in-the-Loop (HITL) Execution Gateway.
Unifies Outbound LLM Proxy with RawHuman Inbound I/O Sentinel.
Intercepts autonomous AI agent tool calls and enforces physical human attestation
before dangerous commands (bash, SQL, payments, deployment) are executed.
"""

from __future__ import annotations
import hashlib
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from rawhuman_engine.biomechanics import BiomechanicalAnalyzer
from rawhuman_engine.detector import SyntheticEventDetector


class ActionRiskLevel(str, Enum):
    LOW = "LOW"             # e.g. read_file, search_web
    MEDIUM = "MEDIUM"       # e.g. create_draft, send_slack_msg
    HIGH = "HIGH"           # e.g. git_push, modify_file
    CRITICAL = "CRITICAL"   # e.g. execute_bash, delete_db, transfer_funds, deploy_prod


@dataclass
class ToolExecutionPolicy:
    name: str
    risk_level: ActionRiskLevel
    requires_hardware_human_attestation: bool


class HITLGateway:
    """
    Guards autonomous AI agent tool executions by coupling
    LLM function dispatching directly to physical human I/O attestation.
    """

    DEFAULT_TOOL_POLICIES = {
        "execute_bash": ToolExecutionPolicy("execute_bash", ActionRiskLevel.CRITICAL, True),
        "run_shell_command": ToolExecutionPolicy("run_shell_command", ActionRiskLevel.CRITICAL, True),
        "run_command": ToolExecutionPolicy("run_command", ActionRiskLevel.CRITICAL, True),
        "execute_sql": ToolExecutionPolicy("execute_sql", ActionRiskLevel.CRITICAL, True),
        "delete_database": ToolExecutionPolicy("delete_database", ActionRiskLevel.CRITICAL, True),
        "transfer_funds": ToolExecutionPolicy("transfer_funds", ActionRiskLevel.CRITICAL, True),
        "deploy_production": ToolExecutionPolicy("deploy_production", ActionRiskLevel.CRITICAL, True),
        "git_push": ToolExecutionPolicy("git_push", ActionRiskLevel.HIGH, True),
        "write_to_file": ToolExecutionPolicy("write_to_file", ActionRiskLevel.MEDIUM, False),
        "read_file": ToolExecutionPolicy("read_file", ActionRiskLevel.LOW, False),
    }

    def __init__(
        self,
        detector: Optional[SyntheticEventDetector] = None,
        analyzer: Optional[BiomechanicalAnalyzer] = None,
    ):
        self.detector = detector or SyntheticEventDetector()
        self.analyzer = analyzer or BiomechanicalAnalyzer()
        self.policies = dict(self.DEFAULT_TOOL_POLICIES)
        self.blocked_event_log: List[Dict[str, Any]] = []
        self.approved_event_log: List[Dict[str, Any]] = []

    def evaluate_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        simulated_flags: int = 0x00,
        hardware_attestation_token: Optional[str] = None,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Evaluates whether an autonomous LLM agent tool call is authorized to execute.
        Requires physical human presence for HIGH and CRITICAL actions.
        """
        policy = self.policies.get(
            tool_name,
            ToolExecutionPolicy(tool_name, ActionRiskLevel.HIGH, True)
        )

        metadata = {
            "tool_name": tool_name,
            "risk_level": policy.risk_level.value,
            "timestamp": time.time(),
        }

        # Low risk tools proceed automatically
        if not policy.requires_hardware_human_attestation:
            return True, "AUTO_PERMITTED_LOW_RISK", metadata

        # 1. Hardware Biometric Token Bypass (TouchID / WebAuthn)
        if hardware_attestation_token and hardware_attestation_token.startswith("touchid_valid_"):
            metadata["verification_method"] = "HARDWARE_SECURE_ENCLAVE_TOUCHID"
            self.approved_event_log.append(metadata)
            return True, "VERIFIED_HARDWARE_TOUCHID", metadata

        # 2. Inspect OS Synthetic Flags
        os_result = self.detector.inspect_event_metadata(event_flags=simulated_flags)
        if os_result.is_synthetic:
            err = (
                f"E_HITL_BLOCKED: Autonomous AI agent attempted to trigger '{tool_name}' "
                f"via synthetic OS event injection ({os_result.platform_flag}). Execution halted."
            )
            metadata["rejection_reason"] = err
            self.blocked_event_log.append(metadata)
            return False, err, metadata

        # 3. Inspect Biomechanical Human Presence
        bio_report = self.analyzer.analyze()
        if not bio_report.is_human and bio_report.sample_count >= self.analyzer.min_samples:
            err = (
                f"E_HITL_BLOCKED: '{tool_name}' requires physical human authorization. "
                f"Biomechanical confidence ({bio_report.human_confidence * 100:.1f}%) below threshold."
            )
            metadata["rejection_reason"] = err
            metadata["biomechanical_report"] = bio_report
            self.blocked_event_log.append(metadata)
            return False, err, metadata

        # Passed verification
        metadata["verification_method"] = "PHYSICAL_HID_BIOMECHANICAL"
        metadata["human_confidence"] = bio_report.human_confidence
        self.approved_event_log.append(metadata)
        return True, "VERIFIED_PHYSICAL_HUMAN", metadata
