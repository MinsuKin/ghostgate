"""
GhostGate Core: Workstation AI Privacy & Security Auditor.
Scans developer environments (Cursor, VS Code, Shell, .env files)
to evaluate AI leak vulnerability and assign an objective security grade (A+ to F).
"""

from __future__ import annotations
import json
import os
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class AuditFinding:
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW", "PASS"
    title: str
    description: str
    remediation: Optional[str] = None


@dataclass
class AuditReport:
    grade: str
    score: int  # 0 to 100
    findings: List[AuditFinding] = field(default_factory=list)
    environment_summary: Dict[str, Any] = field(default_factory=dict)


class WorkstationAuditor:
    """
    Scans the local workstation for unencrypted AI data exfiltration vectors.
    """

    def __init__(self, home_dir: Optional[str] = None):
        self.home = Path(home_dir) if home_dir else Path.home()
        self.os_type = platform.system()

    def audit_all(self) -> AuditReport:
        findings: List[AuditFinding] = []
        score = 100

        # 1. Audit Shell Environment Variables
        env_findings, env_deductions = self._audit_environment_variables()
        findings.extend(env_findings)
        score -= env_deductions

        # 2. Audit Cursor IDE Privacy Settings
        cursor_findings, cursor_deductions = self._audit_cursor_settings()
        findings.extend(cursor_findings)
        score -= cursor_deductions

        # 3. Audit VS Code Telemetry & Copilot Settings
        vscode_findings, vscode_deductions = self._audit_vscode_settings()
        findings.extend(vscode_findings)
        score -= vscode_deductions

        # 4. Audit Local .env Files
        envfile_findings, envfile_deductions = self._audit_local_env_files()
        findings.extend(envfile_findings)
        score -= envfile_deductions

        score = max(0, min(100, score))
        grade = self._score_to_grade(score)

        return AuditReport(
            grade=grade,
            score=score,
            findings=findings,
            environment_summary={
                "os": self.os_type,
                "home": str(self.home),
                "openai_base_url": os.environ.get("OPENAI_BASE_URL", "NOT_CONFIGURED (Defaulting to api.openai.com)"),
                "ghostgate_proxy_active": self._is_proxy_active(),
            },
        )

    def _score_to_grade(self, score: int) -> str:
        if score >= 95:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 75:
            return "B"
        elif score >= 65:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def _is_proxy_active(self) -> bool:
        base_url = os.environ.get("OPENAI_BASE_URL", "")
        return "127.0.0.1:8080" in base_url or "localhost:8080" in base_url

    def _audit_environment_variables(self) -> tuple[List[AuditFinding], int]:
        findings = []
        deductions = 0

        base_url = os.environ.get("OPENAI_BASE_URL", "")
        has_openai_key = bool(os.environ.get("OPENAI_API_KEY"))

        if has_openai_key and not ("127.0.0.1:8080" in base_url or "localhost:8080" in base_url):
            findings.append(
                AuditFinding(
                    severity="CRITICAL",
                    title="Direct Cloud LLM Egress without Proxy",
                    description="OPENAI_API_KEY is active in shell, but OPENAI_BASE_URL does not route through GhostGate (localhost:8080). Prompts are exfiltrated directly to cloud servers with 30-day log retention.",
                    remediation='export OPENAI_BASE_URL="http://127.0.0.1:8080/v1"',
                )
            )
            deductions += 30
        elif "127.0.0.1:8080" in base_url or "localhost:8080" in base_url:
            findings.append(
                AuditFinding(
                    severity="PASS",
                    title="Shell AI Traffic Routed to GhostGate",
                    description="OPENAI_BASE_URL is actively configured to route through GhostGate local privacy proxy.",
                )
            )

        return findings, deductions

    def _audit_cursor_settings(self) -> tuple[List[AuditFinding], int]:
        findings = []
        deductions = 0

        # Locate Cursor settings.json
        if self.os_type == "Darwin":
            cursor_path = self.home / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
        elif self.os_type == "Windows":
            cursor_path = Path(os.environ.get("APPDATA", "")) / "Cursor" / "User" / "settings.json"
        else:
            cursor_path = self.home / ".config" / "Cursor" / "User" / "settings.json"

        if cursor_path.exists():
            try:
                with open(cursor_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    privacy_mode = settings.get("cursor.privacyMode", False)
                    if not privacy_mode:
                        findings.append(
                            AuditFinding(
                                severity="HIGH",
                                title="Cursor IDE Privacy Mode Disabled",
                                description="Cursor IDE is configured with Privacy Mode OFF. Prompts and codebase context may be retained or trained on by remote infrastructure.",
                                remediation='Set "cursor.privacyMode": true in Cursor settings.json',
                            )
                        )
                        deductions += 25
                    else:
                        findings.append(
                            AuditFinding(
                                severity="PASS",
                                title="Cursor IDE Privacy Mode Enabled",
                                description="Cursor IDE has Privacy Mode strictly set to true.",
                            )
                        )
            except Exception:
                pass
        else:
            findings.append(
                AuditFinding(
                    severity="PASS",
                    title="Cursor IDE Not Detected",
                    description="Cursor configuration file was not found in standard user paths.",
                )
            )

        return findings, deductions

    def _audit_vscode_settings(self) -> tuple[List[AuditFinding], int]:
        findings = []
        deductions = 0

        if self.os_type == "Darwin":
            vscode_path = self.home / "Library" / "Application Support" / "Code" / "User" / "settings.json"
        elif self.os_type == "Windows":
            vscode_path = Path(os.environ.get("APPDATA", "")) / "Code" / "User" / "settings.json"
        else:
            vscode_path = self.home / ".config" / "Code" / "User" / "settings.json"

        if vscode_path.exists():
            try:
                with open(vscode_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    telemetry = settings.get("telemetry.telemetryLevel", "all")
                    if telemetry != "off":
                        findings.append(
                            AuditFinding(
                                severity="MEDIUM",
                                title="VS Code Telemetry Active",
                                description=f"VS Code telemetry is set to '{telemetry}'. Client fingerprints and usage data are sent to Microsoft servers.",
                                remediation='Set "telemetry.telemetryLevel": "off" in VS Code settings.json',
                            )
                        )
                        deductions += 15
                    else:
                        findings.append(
                            AuditFinding(
                                severity="PASS",
                                title="VS Code Telemetry Disabled",
                                description="VS Code telemetry is disabled ('off').",
                            )
                        )
            except Exception:
                pass

        return findings, deductions

    def _audit_local_env_files(self) -> tuple[List[AuditFinding], int]:
        findings = []
        deductions = 0

        cwd = Path.cwd()
        env_files = list(cwd.glob("**/.env*"))
        # Exclude .venv
        filtered_env_files = [f for f in env_files if ".venv" not in str(f) and "node_modules" not in str(f)]

        if filtered_env_files:
            for env_path in filtered_env_files[:3]:
                try:
                    with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "AKIA" in content or "sk-" in content or "password" in content.lower():
                            findings.append(
                                AuditFinding(
                                    severity="HIGH",
                                    title=f"Unencrypted Secrets in Local File: {env_path.name}",
                                    description=f"Plaintext credentials found in {env_path}. If pasted into AI prompts, these secrets will be exfiltrated.",
                                    remediation=f"Mask sensitive tokens or ensure GhostGate Proxy is running before querying LLMs.",
                                )
                            )
                            deductions += 15
                            break
                except Exception:
                    pass

        return findings, deductions
