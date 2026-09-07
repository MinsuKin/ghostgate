import pytest
from pathlib import Path
from ghostgate_core.auditor import WorkstationAuditor, AuditReport


def test_workstation_auditor_grading(tmp_path: Path, monkeypatch):
    # Set mock home directory
    auditor = WorkstationAuditor(home_dir=str(tmp_path))

    # Mock environment variables with GhostGate active
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:8080/v1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-mock-key")

    report: AuditReport = auditor.audit_all()

    assert report.grade in ("A+", "A", "B")
    assert report.score >= 70
    assert report.environment_summary["ghostgate_proxy_active"] is True
    assert any(f.severity == "PASS" for f in report.findings)


def test_workstation_auditor_detects_unprotected_egress(tmp_path: Path, monkeypatch):
    auditor = WorkstationAuditor(home_dir=str(tmp_path))

    # Mock environment variables without GhostGate proxy
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-mock-key")

    report: AuditReport = auditor.audit_all()

    assert report.environment_summary["ghostgate_proxy_active"] is False
    assert any(f.severity == "CRITICAL" and "Direct Cloud LLM Egress" in f.title for f in report.findings)
    assert report.score <= 80
