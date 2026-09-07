"""
Mock Upstream OpenAI/Anthropic Server for Local & E2E Testing.
Runs an async mock LLM server on port 9000 to verify zero data leakage,
request sanitization, and streaming response rehydration.
"""

import json
import os
import time
from typing import Any, AsyncGenerator, Dict, List, Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn

app = FastAPI(title="Mock LLM Upstream Server")

last_received_payload: Optional[Dict[str, Any]] = None
last_received_headers: Optional[Dict[str, str]] = None
all_received_requests: List[Dict[str, Any]] = []


@app.get("/health")
async def health():
    return {"status": "mock_upstream_active"}


@app.get("/inspect/last_request")
async def inspect_last():
    return {
        "headers": last_received_headers,
        "payload": last_received_payload,
        "total_count": len(all_received_requests),
    }


@app.post("/inspect/reset")
async def reset_inspect():
    global last_received_payload, last_received_headers, all_received_requests
    last_received_payload = None
    last_received_headers = None
    all_received_requests.clear()
    return {"status": "cleared"}


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "gpt-4o", "object": "model", "owned_by": "mock-system"},
            {"id": "claude-3-5-sonnet", "object": "model", "owned_by": "mock-system"},
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    global last_received_payload, last_received_headers
    raw_body = await request.body()
    payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
    last_received_payload = payload
    last_received_headers = dict(request.headers)
    all_received_requests.append(payload)

    # Extract user prompt
    messages = payload.get("messages", [])
    user_prompt = ""
    for m in messages:
        if m.get("role") == "user":
            user_prompt = m.get("content", "")

    is_stream = payload.get("stream", False)
    echo_reply = f"Mock LLM Response echo: {user_prompt}"

    if is_stream:
        async def sse_stream() -> AsyncGenerator[bytes, None]:
            words = echo_reply.split(" ")
            for i, word in enumerate(words):
                chunk = {
                    "id": "chatcmpl-mock-chunk",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": payload.get("model", "gpt-4o"),
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": (word + " ") if i < len(words) - 1 else word},
                            "finish_reason": None,
                        }
                    ],
                }
                yield f"data: {json.dumps(chunk)}\n\n".encode("utf-8")
            # End chunk
            end_chunk = {
                "id": "chatcmpl-mock-chunk",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": payload.get("model", "gpt-4o"),
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            yield f"data: {json.dumps(end_chunk)}\n\n".encode("utf-8")
            yield b"data: [DONE]\n\n"

        return StreamingResponse(
            sse_stream(),
            media_type="text/event-stream",
            headers={"Content-Type": "text/event-stream"},
        )

    # Non-streaming response
    return JSONResponse({
        "id": "chatcmpl-mock-single",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.get("model", "gpt-4o"),
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": echo_reply},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(user_prompt.split()),
            "completion_tokens": len(echo_reply.split()),
            "total_tokens": len(user_prompt.split()) + len(echo_reply.split()),
        },
    })


def main():
    host = os.environ.get("MOCK_UPSTREAM_HOST", "0.0.0.0")
    port = int(os.environ.get("MOCK_UPSTREAM_PORT", 9000))
    uvicorn.run("tests.mock_upstream:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
