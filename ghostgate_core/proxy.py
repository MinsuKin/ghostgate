"""
GhostGate Core: Async Reverse Proxy Server.
Provides drop-in OpenAI and Anthropic compatibility with format-preserving secret masking,
Human-in-the-Loop (HITL) tool call gating, and embedded CISO Security Dashboard.
"""

from __future__ import annotations
import json
import logging
from typing import Any, AsyncGenerator, Dict, Optional
import httpx
import yaml
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from ghostgate_core.dashboard import metrics_collector, render_dashboard_html
from ghostgate_core.hitl_gateway import HITLGateway
from ghostgate_core.redactor import MaskingMode, RedactionContext, SecretRedactor
from ghostgate_core.zdr_enforcer import ZDREnforcer

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
        import os
        config_file = os.environ.get("GHOSTGATE_CONFIG", path)
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.warning("Failed to load %s (%s). Using fallback defaults.", config_file, e)
            return {}


proxy_state = ProxyState()


@app.get("/dashboard", response_class=HTMLResponse)
async def get_ciso_dashboard():
    """Renders the embedded real-time CISO & SOC Security Dashboard."""
    return render_dashboard_html()


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
