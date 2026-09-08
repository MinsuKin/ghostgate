"""
GhostGate Official Reproducible Benchmark Harness.
Measures latency (P50, P90, P99), throughput, and memory allocations
across variable payload sizes and streaming token rehydration.
"""

from __future__ import annotations
import gc
import json
import os
import platform
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Dict, List

from ghostgate_core.redactor import SecretRedactor, MaskingMode
from rawhuman_engine.biomechanics import (
    BiomechanicalAnalyzer,
    generate_human_like_trajectory,
)

# Test Payloads
SMALL_PAYLOAD = (
    "Please debug my AWS S3 client:\n"
    "AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'\n"
    "client.get_object(Bucket='finance-2026', Key='q4.csv')"
)

MEDIUM_PAYLOAD = (
    "# Multi-service deployment configuration\n"
    "AWS_KEY='AKIAIOSFODNN7EXAMPLE'\n"
    "AWS_SECRET='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'\n"
    "DATABASE_URL='postgres://app_user:SuperSecretPass123!@10.0.1.25:5432/core_banking'\n"
    "ADMIN_EMAIL='security.lead@internal-corp.net'\n"
    "GATEWAY_IP='198.51.100.45'\n"
    "GITHUB_DEPLOY_TOKEN='ghp_1234567890abcdef1234567890abcdef123456'\n"
    "def connect_all():\n"
    "    print('Connecting to database and external APIs with above credentials')\n"
    "    return True\n"
) * 3  # ~1.2 KB

LARGE_PAYLOAD = (
    "# Large application codebase configuration module\n"
    "import os, boto3, psycopg2, redis\n\n"
    + MEDIUM_PAYLOAD * 8  # ~10 KB
)


def compute_percentiles(times_ms: List[float]) -> Dict[str, float]:
    sorted_times = sorted(times_ms)
    n = len(sorted_times)
    return {
        "min_ms": round(sorted_times[0], 4),
        "p50_ms": round(statistics.median(sorted_times), 4),
        "p90_ms": round(sorted_times[int(n * 0.90)], 4),
        "p99_ms": round(sorted_times[int(n * 0.99)], 4),
        "max_ms": round(sorted_times[-1], 4),
        "mean_ms": round(statistics.mean(sorted_times), 4),
        "stddev_ms": round(statistics.stdev(sorted_times), 4) if n > 1 else 0.0,
    }


def benchmark_redaction(
    payload: str,
    iterations: int = 1000,
    warmup: int = 100,
) -> Dict[str, Any]:
    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)

    # Warmup
    for _ in range(warmup):
        redactor.redact_text(payload)

    # Measurement
    latencies_ms = []
    gc.disable()
    t_start = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter()
        redacted, ctx = redactor.redact_text(payload)
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)
    t_total = time.perf_counter() - t_start
    gc.enable()

    stats = compute_percentiles(latencies_ms)
    payload_size_kb = len(payload.encode("utf-8")) / 1024.0
    throughput_mb_s = (payload_size_kb * iterations / 1024.0) / t_total
    ops_sec = iterations / t_total

    stats["ops_per_sec"] = round(ops_sec, 1)
    stats["throughput_mb_per_sec"] = round(throughput_mb_s, 2)
    stats["payload_bytes"] = len(payload.encode("utf-8"))
    return stats


def benchmark_rehydration(
    payload: str,
    iterations: int = 1000,
    warmup: int = 100,
) -> Dict[str, Any]:
    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    redacted, ctx = redactor.redact_text(payload)

    # Warmup
    for _ in range(warmup):
        redactor.rehydrate_text(redacted, ctx)

    latencies_ms = []
    gc.disable()
    for _ in range(iterations):
        t0 = time.perf_counter()
        redactor.rehydrate_text(redacted, ctx)
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)
    gc.enable()

    stats = compute_percentiles(latencies_ms)
    return stats


def benchmark_kinematic_eval(
    iterations: int = 1000,
    warmup: int = 100,
) -> Dict[str, Any]:
    points = generate_human_like_trajectory((10.0, 20.0), (800.0, 600.0), steps=25)

    # Warmup
    for _ in range(warmup):
        analyzer = BiomechanicalAnalyzer(min_samples=8)
        for p in points:
            analyzer.add_point(p.x, p.y, p.timestamp)
        analyzer.analyze()

    latencies_ms = []
    gc.disable()
    for _ in range(iterations):
        analyzer = BiomechanicalAnalyzer(min_samples=8)
        for p in points:
            analyzer.add_point(p.x, p.y, p.timestamp)
        t0 = time.perf_counter()
        analyzer.analyze()
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)
    gc.enable()

    stats = compute_percentiles(latencies_ms)
    return stats


def benchmark_memory_alloc(payload: str, iterations: int = 1000) -> Dict[str, Any]:
    tracemalloc.start()
    redactor = SecretRedactor(mode=MaskingMode.FORMAT_PRESERVING)
    for _ in range(iterations):
        redacted, ctx = redactor.redact_text(payload)
    current_b, peak_b = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "current_kb": round(current_b / 1024.0, 2),
        "peak_kb": round(peak_b / 1024.0, 2),
    }


def main():
    print("=" * 80)
    print("  GHOSTGATE REPRODUCIBLE BENCHMARK SUITE")
    print(f"  Platform : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  Python   : {sys.version.split()[0]} ({platform.python_implementation()})")
    print("=" * 80)

    results = {
        "metadata": {
            "os": platform.system(),
            "machine": platform.machine(),
            "python": sys.version.split()[0],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "iterations_per_test": 1000,
            "warmup_iterations": 100,
        },
        "benchmarks": {},
    }

    print("\n[1/4] Measuring Format-Preserving Masking Latency (1,000 iterations)...")
    results["benchmarks"]["small_payload_masking"] = benchmark_redaction(SMALL_PAYLOAD)
    results["benchmarks"]["medium_payload_masking"] = benchmark_redaction(MEDIUM_PAYLOAD)
    results["benchmarks"]["large_payload_masking"] = benchmark_redaction(LARGE_PAYLOAD)

    print("\n[2/4] Measuring In-Memory Rehydration Overhead (1,000 iterations)...")
    results["benchmarks"]["medium_payload_rehydration"] = benchmark_rehydration(MEDIUM_PAYLOAD)

    print("\n[3/4] Measuring Kinematic Trajectory Evaluation Latency (1,000 iterations)...")
    results["benchmarks"]["kinematic_trajectory_eval"] = benchmark_kinematic_eval()

    print("\n[4/4] Profiling Memory Allocation (tracemalloc)...")
    results["benchmarks"]["memory_profile"] = benchmark_memory_alloc(MEDIUM_PAYLOAD)

    # Save to json
    out_path = Path(__file__).parent / "benchmark_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Print Summary Table
    print("\n" + "=" * 80)
    print("  BENCHMARK RESULTS SUMMARY (Latency in milliseconds)")
    print("=" * 80)
    print(f"{'Test Case':<32} {'Payload':<10} {'P50 (ms)':<10} {'P90 (ms)':<10} {'P99 (ms)':<10} {'Throughput'}")
    print("-" * 80)

    for name, r in results["benchmarks"].items():
        if "p50_ms" in r:
            payload_str = f"{r.get('payload_bytes', '-')} B"
            tp_str = f"{r.get('ops_per_sec', '-')} ops/s" if "ops_per_sec" in r else "-"
            print(f"{name:<32} {payload_str:<10} {r['p50_ms']:<10.4f} {r['p90_ms']:<10.4f} {r['p99_ms']:<10.4f} {tp_str}")

    mem = results["benchmarks"]["memory_profile"]
    print("-" * 80)
    print(f"Peak Memory Allocated during 1,000-cycle batch: {mem['peak_kb']} KB")
    print(f"Results recorded to: {out_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
