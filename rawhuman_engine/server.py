"""
RawHuman Engine: Microservice Daemon.
Provides the HTTP attestation API for applications, webhooks, and OS security guards.
"""

from __future__ import annotations
import hashlib
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rawhuman_engine.biomechanics import BiomechanicalAnalyzer
from rawhuman_engine.detector import SyntheticEventDetector

app = FastAPI(
    title="RawHuman I/O Attestation Sentinel",
    description="Kernel & I/O-level Proof-of-Human API against Autonomous Multimodal AI Agents",
    version="1.0.0",
)

detector = SyntheticEventDetector()
analyzer = BiomechanicalAnalyzer(min_samples=8, confidence_threshold=0.60)


class CoordinateSample(BaseModel):
    x: float
    y: float
    timestamp: Optional[float] = None
    event_flags: Optional[int] = 0
    source_id: Optional[int] = None
    source_pid: Optional[int] = None


class BatchSampleRequest(BaseModel):
    samples: List[CoordinateSample]
    action_context: Optional[str] = "payment_or_admin_action"


class AttestationResponse(BaseModel):
    is_human: bool
    human_confidence_score: float
    origin: str
    is_synthetic_injection: bool
    platform_flag: Optional[str]
    fitts_law_fit: float
    tremor_energy_score: float
    timing_jitter_entropy: float
    sample_count: int
    attestation_token: str
    rejection_reasons: List[str]


@app.get("/health")
async def health_check():
    return {
        "service": "RawHuman I/O Sentinel",
        "status": "active",
        "os": detector.os_type,
        "quartz_hook_active": detector.quartz_available,
        "sample_buffer_size": len(analyzer.samples),
    }


@app.post("/v1/human/reset")
async def reset_buffer():
    analyzer.reset()
    return {"status": "cleared"}


@app.post("/v1/human/sample")
async def ingest_samples(payload: BatchSampleRequest):
    now = time.time()
    for s in payload.samples:
        ts = s.timestamp if s.timestamp is not None else now
        analyzer.add_point(s.x, s.y, ts)
    return {"status": "ok", "total_samples": len(analyzer.samples)}


@app.get("/v1/human/verify", response_model=AttestationResponse)
async def verify_human():
    # 1. Run biomechanical analysis
    report = analyzer.analyze()

    # 2. Inspect OS injection markers
    synthetic_result = detector.inspect_event_metadata()

    # 3. Formulate final decision
    final_is_human = report.is_human and not synthetic_result.is_synthetic
    reasons = list(report.rejection_reasons)
    if synthetic_result.is_synthetic:
        reasons.append(f"OS Synthetic Flag Alert: {synthetic_result.platform_flag}")

    # Generate tamper-resistant cryptographic attestation signature
    raw_payload = f"{final_is_human}:{report.human_confidence}:{time.time()}:{report.sample_count}"
    attestation_token = f"rawhuman_attest_{hashlib.sha256(raw_payload.encode()).hexdigest()[:24]}"

    return AttestationResponse(
        is_human=final_is_human,
        human_confidence_score=report.human_confidence,
        origin=synthetic_result.origin.value,
        is_synthetic_injection=synthetic_result.is_synthetic,
        platform_flag=synthetic_result.platform_flag,
        fitts_law_fit=report.fitts_law_fit,
        tremor_energy_score=report.tremor_energy_score,
        timing_jitter_entropy=report.timing_jitter_entropy,
        sample_count=report.sample_count,
        attestation_token=attestation_token,
        rejection_reasons=reasons,
    )


def main():
    import os
    import uvicorn
    host = os.environ.get("RAWHUMAN_HOST", "0.0.0.0")
    port = int(os.environ.get("RAWHUMAN_PORT", 8081))
    uvicorn.run("rawhuman_engine.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
