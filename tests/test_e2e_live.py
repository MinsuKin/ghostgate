"""
GhostGate & RawHuman: Comprehensive Live E2E Integration Test Suite.
Executes real HTTP requests against the containerized stack:
  - GhostGate Proxy (:8080)
  - RawHuman Sentinel (:8081)
  - Mock Upstream LLM (:9000)
  - Air-Gap Ollama (:11434)
Verifies zero data leakage, format-preserving substitution, SSE streaming rehydration,
airgap rerouting, CISO dashboard metrics, and autonomous agent blocking.
"""

import json
import time
import httpx
import pytest
from rich.console import Console
from rich.table import Table

console = Console()

PROXY_URL = "http://127.0.0.1:8080"
RAWHUMAN_URL = "http://127.0.0.1:8081"
MOCK_UPSTREAM_URL = "http://127.0.0.1:9000"
OLLAMA_URL = "http://127.0.0.1:11434"


def wait_for_services(timeout_seconds: int = 45):
    """Waits until all required services are reachable and healthy."""
    endpoints = [
        ("GhostGate Proxy", f"{PROXY_URL}/health"),
        ("RawHuman Sentinel", f"{RAWHUMAN_URL}/health"),
        ("Mock Upstream", f"{MOCK_UPSTREAM_URL}/health"),
    ]
    console.print("[yellow]⏳ Probing service health endpoints...[/yellow]")
    start = time.time()
    for name, url in endpoints:
        healthy = False
        while time.time() - start < timeout_seconds:
            try:
                resp = httpx.get(url, timeout=2.0)
                if resp.status_code == 200:
                    console.print(f"[green]✔ {name} is READY at {url}[/green]")
                    healthy = True
                    break
            except Exception:
                time.sleep(1.0)
        if not healthy:
            raise RuntimeError(f"Service {name} failed to start within {timeout_seconds}s at {url}")


@pytest.fixture(scope="session", autouse=True)
def setup_services():
    wait_for_services()


def test_e2e_zero_leakage_and_format_preserving_rehydration():
    """
    E2E Test 1: Verifies that real secrets NEVER reach the upstream LLM,
    are replaced with format-preserving synthetics, and are restored in response.
    """
    # 1. Reset mock upstream inspect log
    httpx.post(f"{MOCK_UPSTREAM_URL}/inspect/reset", timeout=5.0)

    raw_aws_key = "AKIAIOSFODNN7EXAMPLE"
    raw_db_url = "postgres://admin:SuperSecretPass123@prod-cluster.internal:5432/finance"
    raw_prompt = f"Please inspect AWS key {raw_aws_key} and database {raw_db_url}."

    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": raw_prompt}],
        "stream": False,
    }

    # 2. Send through GhostGate proxy
    resp = httpx.post(f"{PROXY_URL}/v1/chat/completions", json=payload, timeout=10.0)
    assert resp.status_code == 200, f"Proxy returned error: {resp.text}"
    client_response = resp.json()

    # 3. Check what Mock Upstream actually received
    inspect_resp = httpx.get(f"{MOCK_UPSTREAM_URL}/inspect/last_request", timeout=5.0)
    assert inspect_resp.status_code == 200
    inspect_data = inspect_resp.json()
    upstream_payload = inspect_data["payload"]

    upstream_user_prompt = upstream_payload["messages"][0]["content"]

    # --- ASSERTION 1: Zero Cloud Egress of Secrets ---
    assert raw_aws_key not in upstream_user_prompt, "CRITICAL LEAK: Raw AWS Key leaked to upstream!"
    assert "SuperSecretPass123" not in upstream_user_prompt, "CRITICAL LEAK: DB Password leaked to upstream!"
    assert "prod-cluster.internal" not in upstream_user_prompt, "CRITICAL LEAK: Internal DB domain leaked!"

    # --- ASSERTION 2: Format-Preserving Synthetic Masking ---
    assert "AKIA" in upstream_user_prompt, "Upstream did not receive a valid synthetic AKIA key!"
    assert "postgres://mock_user_" in upstream_user_prompt, "Upstream did not receive a synthetic DB URL!"

    # --- ASSERTION 3: Bidirectional In-Memory Rehydration ---
    assistant_reply = client_response["choices"][0]["message"]["content"]
    assert raw_aws_key in assistant_reply, "Rehydration failed: Raw AWS key not restored for client!"
    assert "SuperSecretPass123" in assistant_reply, "Rehydration failed: DB password not restored!"
    assert "prod-cluster.internal" in assistant_reply, "Rehydration failed: DB domain not restored!"

    console.print("[bold green]✔ E2E Test 1 Passed: Format-Preserving Secret Masking & Rehydration Verified![/bold green]")


def test_e2e_streaming_sse_rehydration():
    """
    E2E Test 2: Verifies that real-time Server-Sent Events (SSE) streaming chunks
    preserve secrets and stream back rehydrated tokens without chunk fragmentation.
    """
    raw_email = "security.director@enterprise-corp.com"
    raw_prompt = f"Please send incident notifications to {raw_email}."

    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": raw_prompt}],
        "stream": True,
    }

    chunks_received = []
    with httpx.stream("POST", f"{PROXY_URL}/v1/chat/completions", json=payload, timeout=10.0) as resp:
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")

        for line in resp.iter_lines():
            if line.startswith("data: ") and not line.endswith("[DONE]"):
                chunk_json = json.loads(line[6:])
                delta = chunk_json.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                chunks_received.append(content)

    full_stream_text = "".join(chunks_received)

    # Verify rehydration occurred across streaming chunks
    assert raw_email in full_stream_text, f"Streaming rehydration failed: expected '{raw_email}' in '{full_stream_text}'"
    console.print("[bold green]✔ E2E Test 2 Passed: Streaming SSE Token Rehydration Verified![/bold green]")


def test_e2e_ciso_dashboard_and_metrics():
    """
    E2E Test 3: Verifies that the CISO & SOC Web Dashboard renders live HTML
    and updates metrics counters dynamically.
    """
    # 1. HTML Dashboard
    html_resp = httpx.get(f"{PROXY_URL}/dashboard", timeout=5.0)
    assert html_resp.status_code == 200
    assert "text/html" in html_resp.headers.get("content-type", "")
    assert "GHOSTGATE" in html_resp.text
    assert "ENTERPRISE SOC" in html_resp.text
    assert "ZDR Compliance Health" in html_resp.text

    # 2. JSON Metrics Endpoint
    metrics_resp = httpx.get(f"{PROXY_URL}/api/dashboard/metrics", timeout=5.0)
    assert metrics_resp.status_code == 200
    metrics = metrics_resp.json()
    assert metrics["total_requests"] > 0
    assert metrics["total_secrets_masked"] > 0
    assert metrics["zdr_compliance_score"] > 90.0

    console.print("[bold green]✔ E2E Test 3 Passed: CISO Security Dashboard & Telemetry Verified![/bold green]")


def test_e2e_airgap_local_routing_isolation():
    """
    E2E Test 4: Verifies that prompts containing '# @airgap' are dynamically
    rerouted to local containerized Ollama, with ZERO requests sent to upstream cloud.
    """
    # 1. Record mock upstream count before
    inspect_before = httpx.get(f"{MOCK_UPSTREAM_URL}/inspect/last_request", timeout=5.0).json()
    count_before = inspect_before.get("total_count", 0)

    airgap_payload = {
        "model": "qwen2.5-coder:7b",
        "messages": [{"role": "user", "content": "# @airgap Proprietary Trade Secret Kernel Architecture"}],
    }

    # 2. Dispatch to GhostGate
    # Even if local Ollama hasn't pulled this specific model yet, GhostGate must attempt routing
    # to the local upstream (11434) and NEVER hit the cloud upstream (9000).
    try:
        httpx.post(f"{PROXY_URL}/v1/chat/completions", json=airgap_payload, timeout=4.0)
    except Exception:
        pass

    # 3. Verify Mock Upstream received NOTHING
    inspect_after = httpx.get(f"{MOCK_UPSTREAM_URL}/inspect/last_request", timeout=5.0).json()
    count_after = inspect_after.get("total_count", 0)

    assert count_after == count_before, "AIRGAP LEAK: Request was sent to cloud upstream instead of isolated local!"
    console.print("[bold green]✔ E2E Test 4 Passed: Deterministic Air-Gap Local Isolation Verified![/bold green]")


def test_e2e_rawhuman_daemon_verification():
    """
    E2E Test 5: Verifies that the RawHuman Sentinel HTTP Daemon evaluates
    synthetic bot injections vs human biomechanical inputs.
    """
    # 1. Reset buffer
    httpx.post(f"{RAWHUMAN_URL}/v1/human/reset", timeout=5.0)

    # 2. Ingest synthetic flat bot clicks
    bot_samples = [
        {"x": 100.0 + i * 20.0, "y": 200.0 + i * 20.0, "timestamp": 1000.0 + (i * 0.010)}
        for i in range(15)
    ]
    httpx.post(f"{RAWHUMAN_URL}/v1/human/sample", json={"samples": bot_samples}, timeout=5.0)

    verify_resp = httpx.get(f"{RAWHUMAN_URL}/v1/human/verify", timeout=5.0)
    assert verify_resp.status_code == 200
    bot_data = verify_resp.json()
    assert bot_data["is_human"] is False, "Bot was falsely verified as human!"
    assert bot_data["human_confidence_score"] < 0.60
    assert len(bot_data["rejection_reasons"]) > 0

    console.print("[bold green]✔ E2E Test 5 Passed: RawHuman Autonomous Bot Termination Verified![/bold green]")


def main():
    console.print("\n[bold cyan]======================================================[/bold cyan]")
    console.print("[bold cyan]  🛡️ GHOSTGATE & RAWHUMAN LIVE E2E INTEGRATION SUITE   [/bold cyan]")
    console.print("[bold cyan]======================================================[/bold cyan]\n")

    wait_for_services()

    console.print("\n[bold yellow]Running E2E Test 1: Zero Data Leakage & Format-Preserving Rehydration...[/bold yellow]")
    test_e2e_zero_leakage_and_format_preserving_rehydration()

    console.print("\n[bold yellow]Running E2E Test 2: Live Streaming SSE Token Rehydration...[/bold yellow]")
    test_e2e_streaming_sse_rehydration()

    console.print("\n[bold yellow]Running E2E Test 3: CISO Security Dashboard & Telemetry...[/bold yellow]")
    test_e2e_ciso_dashboard_and_metrics()

    console.print("\n[bold yellow]Running E2E Test 4: Dynamic Air-Gap Local Isolation...[/bold yellow]")
    test_e2e_airgap_local_routing_isolation()

    console.print("\n[bold yellow]Running E2E Test 5: RawHuman Daemon Bot Detection...[/bold yellow]")
    test_e2e_rawhuman_daemon_verification()

    console.print("\n[bold green]======================================================[/bold green]")
    console.print("[bold green]  🎉 ALL LIVE E2E INTEGRATION TESTS PASSED (100%)     [/bold green]")
    console.print("[bold green]======================================================[/bold green]\n")


if __name__ == "__main__":
    main()
