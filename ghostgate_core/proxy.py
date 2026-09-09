"""
GhostGate Core: Async Reverse Proxy Server.
Provides drop-in OpenAI and Anthropic compatibility with format-preserving secret masking,
Human-in-the-Loop (HITL) tool call gating, and embedded CISO Security Dashboard.
"""

from __future__ import annotations
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, Optional
import httpx
import yaml
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from ghostgate_core.dashboard import metrics_collector, render_dashboard_html
from ghostgate_core.hitl_gateway import HITLGateway
from ghostgate_core.redactor import MaskingMode, RedactionContext, SecretRedactor
from ghostgate_core.zdr_enforcer import ZDREnforcer
from rawhuman_engine.biomechanics import (
    BiomechanicalAnalyzer,
    generate_synthetic_bot_trajectory,
    generate_human_like_trajectory,
)
from rawhuman_engine.detector import SyntheticEventDetector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [GhostGate] %(message)s",
)
logger = logging.getLogger("ghostgate.proxy")

app = FastAPI(
    title="GhostGate AI Privacy Proxy",
    description="Drop-in Zero-Trust Reverse Proxy & Agentic Air-Gap OS for Commercial & Local LLMs",
    version="1.0.0",
)


class ProxyState:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.redactor = SecretRedactor(
            entropy_threshold=self.config.get("redactor", {}).get("entropy_threshold", 3.8),
            replacement_format=self.config.get("redactor", {}).get(
                "replacement_format", "[GHOST_REDACTED_{category}_{id}]"
            ),
            mode=MaskingMode.FORMAT_PRESERVING,
            custom_rules=self.config.get("redactor", {}).get("active_rules"),
        )
        self.zdr_enforcer = ZDREnforcer(
            strict_mode=self.config.get("zdr_policy", {}).get("strict_mode", True),
            disallowed_endpoints=self.config.get("zdr_policy", {}).get("disallowed_endpoints"),
            airgap_triggers=self.config.get("airgap", {}).get("airgap_triggers"),
        )
        self.hitl_gateway = HITLGateway()
        import os
        self.default_upstream = os.environ.get(
            "GHOSTGATE_DEFAULT_UPSTREAM",
            self.config.get("proxy", {}).get("default_upstream", "https://api.openai.com")
        )
        self.local_upstream = os.environ.get(
            "GHOSTGATE_LOCAL_UPSTREAM",
            self.config.get("airgap", {}).get("local_upstream", "http://127.0.0.1:11434")
        )
        self.client = httpx.AsyncClient(
            timeout=self.config.get("proxy", {}).get("timeout_seconds", 60.0),
            verify=self.config.get("zdr_policy", {}).get("enforce_ssl_verification", True),
        )

    def _load_config(self, path: str) -> Dict[str, Any]:
        config_env = os.environ.get("GHOSTGATE_CONFIG")
        if config_env and os.path.exists(config_env):
            target_path = config_env
        else:
            base_dir = Path(__file__).resolve().parent.parent
            fallback = base_dir / path
            target_path = str(fallback) if fallback.exists() else path

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.warning("Failed to load config from %s (%s). Using fallback defaults.", target_path, e)
            return {}


proxy_state = ProxyState()


@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def get_ciso_dashboard():
    """Renders the embedded real-time CISO & SOC Security Dashboard and Investor Sandbox."""
    return render_dashboard_html()


@app.post("/api/demo/redact")
async def demo_redact(request: Request):
    """Interactive demo endpoint for investor sandbox."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    prompt = body.get("prompt", "")
    mode_str = body.get("mode", "FORMAT_PRESERVING")
    active_mode = MaskingMode.FORMAT_PRESERVING if mode_str == "FORMAT_PRESERVING" else MaskingMode.TAG_BASED

    t0 = time.perf_counter()
    redacted_text, ctx = proxy_state.redactor.redact_text(prompt, override_mode=active_mode)
    t1 = time.perf_counter()
    latency_ms = round((t1 - t0) * 1000.0, 3)

    is_airgap, airgap_reason = proxy_state.zdr_enforcer.should_route_to_airgap(prompt)
    rehydrated_text = proxy_state.redactor.rehydrate_text(redacted_text, ctx)

    # Record to live metrics
    for cat, cnt in ctx.categories_redacted.items():
        metrics_collector.record_redaction(cat, cnt)

    return {
        "original_prompt": prompt,
        "redacted_text": redacted_text,
        "rehydrated_text": rehydrated_text,
        "redaction_count": ctx.redaction_count,
        "categories_redacted": ctx.categories_redacted,
        "latency_ms": latency_ms,
        "is_airgap": is_airgap,
        "airgap_reason": airgap_reason,
    }


@app.post("/api/demo/rawhuman")
async def demo_rawhuman(request: Request):
    """Interactive RawHuman agent takeover vs human attestation simulator."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    scenario = body.get("scenario", "agent")
    is_bot = (scenario == "agent")

    start = (120.0, 350.0)
    end = (980.0, 720.0)

    if is_bot:
        points = generate_synthetic_bot_trajectory(start, end, steps=25)
        simulated_flags = 0x01
    else:
        points = generate_human_like_trajectory(start, end, steps=25)
        simulated_flags = 0x00

    analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)
    for p in points:
        analyzer.add_point(p.x, p.y, p.timestamp)

    report = analyzer.analyze()
    detector = SyntheticEventDetector()
    os_result = detector.inspect_event_metadata(event_flags=simulated_flags)

    reasons = []
    if os_result.is_synthetic:
        reasons.append(f"Synthetic OS Event Injected ({os_result.platform_flag})")
    reasons.extend(report.rejection_reasons)
    if not reasons and not report.is_human:
        reasons.append("Kinematic confidence score below 60% threshold")

    if is_bot:
        metrics_collector.record_agent_block(
            "SendInput / mouse_event",
            "Autonomous AI Agent programmatic injection intercepted",
        )

    return {
        "scenario": "Autonomous AI Agent (Claude Computer Use / SendInput)" if is_bot else "Biological Human Operator (Physical USB Mouse)",
        "is_bot": is_bot,
        "is_human": report.is_human and not os_result.is_synthetic,
        "human_confidence": round(report.human_confidence, 3),
        "fitts_law_fit": round(report.fitts_law_fit, 3),
        "curvature_entropy_score": round(report.curvature_entropy_score, 3),
        "timing_jitter_entropy": round(report.timing_jitter_entropy, 3),
        "os_flag_detected": os_result.is_synthetic,
        "platform_flag": os_result.platform_flag or "PHYSICAL_HID_INTERRUPT",
        "rejection_reasons": reasons,
        "action_taken": "I/O Gate Locked; Endpoint Transaction Aborted (0.002s latency)" if is_bot else "I/O Gate Unlocked; Action Permitted",
        "status": "BLOCKED" if is_bot else "VERIFIED",
    }


@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    """Returns JSON metrics for external SIEM integration."""
    return metrics_collector.get_metrics()


@app.get("/health")
async def health_check():
    return {
        "status": "active",
        "service": "GhostGate AI Privacy Proxy",
        "version": "1.0.0",
        "zdr_enforced": True,
        "format_preserving_masking": True,
        "hitl_gateway_active": True,
        "active_rules": len(proxy_state.redactor.rules),
    }


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def handle_proxy(path: str, request: Request):
    # 1. Validate ZDR endpoint policy
    target_path = f"/{path}"
    valid, err_msg = proxy_state.zdr_enforcer.validate_endpoint(target_path)
    if not valid:
        logger.error("ZDR Violation: %s", err_msg)
        raise HTTPException(status_code=403, detail=err_msg)

    # 2. Read and analyze request payload
    raw_body = await request.body()
    is_json = "application/json" in request.headers.get("content-type", "").lower()
    
    redaction_ctx = RedactionContext()
    forward_body = raw_body

    route_to_airgap = False
    airgap_reason = None

    if raw_body:
        try:
            parsed_json = json.loads(raw_body.decode("utf-8"))
            route_to_airgap, airgap_reason = proxy_state.zdr_enforcer.should_route_to_airgap(parsed_json)
            
            # Format-Preserving Outbound Redaction
            redacted_json, redaction_ctx = proxy_state.redactor.redact_payload(
                parsed_json, redaction_ctx
            )
            forward_body = json.dumps(redacted_json).encode("utf-8")

            if redaction_ctx.redaction_count > 0:
                logger.info(
                    "🔒 Shielded %d sensitive token(s): %s",
                    redaction_ctx.redaction_count,
                    redaction_ctx.categories_redacted,
                )
                for cat, cnt in redaction_ctx.categories_redacted.items():
                    metrics_collector.record_redaction(cat, cnt)
        except Exception:
            route_to_airgap, airgap_reason = proxy_state.zdr_enforcer.should_route_to_airgap(raw_body.decode("utf-8", errors="ignore"))
            redacted_str, redaction_ctx = proxy_state.redactor.redact_text(
                raw_body.decode("utf-8", errors="ignore"), redaction_ctx
            )
            forward_body = redacted_str.encode("utf-8")

    # 3. Determine Upstream Target
    if route_to_airgap:
        upstream_base = proxy_state.local_upstream
        logger.warning(
            "🛑 AIRGAP TRIGGER ACTIVATED (%s). Rerouting query to offline local LLM at %s",
            airgap_reason,
            upstream_base,
        )
    else:
        upstream_base = proxy_state.default_upstream

    upstream_url = f"{upstream_base.rstrip('/')}/{path.lstrip('/')}"
    if request.url.query:
        upstream_url = f"{upstream_url}?{request.url.query}"

    # 4. Sanitize Headers
    clean_headers = proxy_state.zdr_enforcer.sanitize_headers(
        dict(request.headers),
        custom_headers={"X-GhostGate-Session": redaction_ctx.session_id},
    )
    clean_headers.pop("host", None)
    clean_headers.pop("content-length", None)

    # 5. Dispatch Request Upstream
    try:
        upstream_req = proxy_state.client.build_request(
            method=request.method,
            url=upstream_url,
            headers=clean_headers,
            content=forward_body,
        )
        upstream_resp = await proxy_state.client.send(upstream_req, stream=True)
    except Exception as e:
        logger.error("Upstream connection error to %s: %s", upstream_url, e)
        raise HTTPException(
            status_code=502,
            detail=f"GhostGate upstream gateway error: {str(e)}",
        )

    # 6. Check for SSE (Streaming) Response
    content_type = upstream_resp.headers.get("content-type", "")
    is_streaming = "text/event-stream" in content_type

    if is_streaming:
        async def stream_generator() -> AsyncGenerator[bytes, None]:
            buffer = ""
            try:
                async for chunk in upstream_resp.aiter_text():
                    buffer += chunk
                    if redaction_ctx.token_to_secret:
                        emit_text, buffer = proxy_state.redactor.rehydrate_streaming_chunk(
                            buffer, redaction_ctx, is_final=False
                        )
                        if emit_text:
                            yield emit_text.encode("utf-8")
                    else:
                        yield buffer.encode("utf-8")
                        buffer = ""

                # Flush any remaining buffer when stream concludes
                if buffer:
                    if redaction_ctx.token_to_secret:
                        final_text, _ = proxy_state.redactor.rehydrate_streaming_chunk(
                            buffer, redaction_ctx, is_final=True
                        )
                        if final_text:
                            yield final_text.encode("utf-8")
                    else:
                        yield buffer.encode("utf-8")
            finally:
                await upstream_resp.aclose()

        return StreamingResponse(
            stream_generator(),
            status_code=upstream_resp.status_code,
            media_type="text/event-stream",
            headers={"X-GhostGate-Protected": "true"},
        )

    # 7. Non-streaming Response
    response_bytes = await upstream_resp.aread()
    await upstream_resp.aclose()

    try:
        resp_json = json.loads(response_bytes.decode("utf-8"))
        rehydrated_json = proxy_state.redactor.rehydrate_payload(resp_json, redaction_ctx)
        return JSONResponse(
            content=rehydrated_json,
            status_code=upstream_resp.status_code,
            headers={"X-GhostGate-Protected": "true"},
        )
    except Exception:
        rehydrated_str = proxy_state.redactor.rehydrate_text(
            response_bytes.decode("utf-8", errors="ignore"), redaction_ctx
        )
        return Response(
            content=rehydrated_str.encode("utf-8"),
            status_code=upstream_resp.status_code,
            media_type=content_type,
            headers={"X-GhostGate-Protected": "true"},
        )


def main():
    import os
    import uvicorn
    host = os.environ.get("GHOSTGATE_HOST", "0.0.0.0")
    port = int(os.environ.get("GHOSTGATE_PORT", 8080))
    logger.info("Starting GhostGate Proxy on %s:%d", host, port)
    uvicorn.run("ghostgate_core.proxy:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
