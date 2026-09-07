import pytest
from httpx import AsyncClient, ASGITransport
from ghostgate_core.proxy import app
from ghostgate_core.zdr_enforcer import ZDREnforcer


@pytest.mark.asyncio
async def test_proxy_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "active"
        assert data["zdr_enforced"] is True
        assert data["format_preserving_masking"] is True
        assert data["hitl_gateway_active"] is True


@pytest.mark.asyncio
async def test_ciso_dashboard_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Test HTML dashboard
        resp = await client.get("/dashboard")
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")
        assert "GhostGate Labs // CISO Security Operations Center" in resp.text

        # Test JSON metrics API
        api_resp = await client.get("/api/dashboard/metrics")
        assert api_resp.status_code == 200
        metrics = api_resp.json()
        assert "total_requests" in metrics
        assert "total_secrets_masked" in metrics
        assert "total_agent_hijacks_blocked" in metrics
        assert metrics["zdr_compliance_score"] > 90.0


@pytest.mark.asyncio
async def test_zdr_policy_blocks_disallowed_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post("/v1/fine_tuning", json={"training_file": "file-123"})
        assert resp.status_code == 403
        assert "blocked by GhostGate ZDR policy" in resp.json()["detail"]


def test_zdr_header_sanitization():
    enforcer = ZDREnforcer()
    dirty_headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "cookie": "session_id=attacker_tracking_cookie",
        "x-stainless-os": "MacOS",
        "x-datadog-trace-id": "994829104",
        "authorization": "Bearer sk-valid-key",
        "content-type": "application/json",
    }

    clean = enforcer.sanitize_headers(dirty_headers)

    assert "cookie" not in clean
    assert "x-stainless-os" not in clean
    assert "x-datadog-trace-id" not in clean
    assert clean["X-GhostGate-ZDR"] == "enforced"
    assert clean["authorization"] == "Bearer sk-valid-key"


def test_airgap_trigger_detection():
    enforcer = ZDREnforcer()
    payload_normal = {"prompt": "Write a python function to sort a list"}
    route, _ = enforcer.should_route_to_airgap(payload_normal)
    assert route is False

    payload_secret = {"prompt": "# @top-secret Internal finance algorithm v2"}
    route, trigger = enforcer.should_route_to_airgap(payload_secret)
    assert route is True
    assert trigger == "# @top-secret"
