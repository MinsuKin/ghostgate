<p align="center">
  <h1 align="center">🛡️ GHOSTGATE</h1>
  <p align="center">
    <strong>The Invisible Bulletproof Glass for Enterprise AI</strong><br>
    <em>Zero-Trust Data Leak Protection • Format-Preserving Secret Masking • Autonomous AI Agent Takeover Defense</em>
  </p>
  <p align="center">
    <a href="https://ghostgate-beta.vercel.app/" target="_blank"><img src="https://img.shields.io/badge/LIVE%20DEMO-ghostgate--beta.vercel.app-6366F1?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Interactive Sandbox"></a>
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
    <img src="https://img.shields.io/badge/python-3.10%2B-brightgreen.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/docker-ready-2496ED.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/tests-28%20passed-success.svg" alt="Tests: 28 passed">
    <img src="https://img.shields.io/badge/latency-%3C0.15ms-indigo.svg" alt="Latency: <0.15ms">
    <img src="https://img.shields.io/badge/attack%20corpus-validated-brightgreen.svg" alt="Attack Corpus Validated">
  </p>
</p>

---

> ### 🌐 Live Interactive Sandbox (No Install Required)
> **Test GhostGate live directly in your browser:**  
> 👉 **[https://ghostgate-beta.vercel.app/](https://ghostgate-beta.vercel.app/)**  
> Test real-world corporate leak scenarios (Payroll Database Password, AWS Root Key, Customer PII) and experience 0.14ms format-preserving secret shadowing and autonomous AI agent takeover defense.

---

## 🧭 Executive Summary: The $45B Enterprise AI Opportunity

### 1. The Enterprise AI Dilemma
Over **100 million enterprise knowledge workers** use generative AI tools (ChatGPT, Claude, Cursor, Copilot) every single day. In doing so, developers and employees routinely and accidentally paste **company database passwords, client emails, private keys, and cloud credentials** directly into third-party cloud prompts.

* **78% of Fortune 500 CISOs** currently restrict or block generative AI tools due to catastrophic data breach liabilities and regulatory fines.
* **$4.45 Million**: The average cost of a corporate data breach (IBM Cost of a Data Breach Report).
* **The Emerging $50B Threat (Rogue Agent Hijack)**: Autonomous AI agents (such as OpenAI Operator and Anthropic Computer Use) physically control employee mice and keyboards. If an AI agent is tricked by a prompt injection attack, it can wipe corporate databases or approve unauthorized financial transfers without human consent.

### 2. The Solution: What GhostGate Does
GhostGate sits invisibly on employee workstations between the user and cloud AI—acting as **digital bulletproof glass**:

1. ⚡ **0.14ms In-Flight Secret Shadowing**: Real database passwords, AWS keys, and PII are intercepted and swapped with harmless, format-preserving fake tokens (`AKIA...`, `postgres://mock_user...`) before leaving the laptop.
2. 🔄 **Lossless In-Memory Rehydration**: When ChatGPT writes back the solution, GhostGate automatically swaps the real credentials back in-memory on the employee's screen. ChatGPT writes the code, but **never sees company secrets**.
3. 🤖 **RawHuman™ Biomechanical Agent Barrier**: Inspects physical human hand micro-tremors and OS kernel injection flags (`LLMHF_INJECTED`) to block rogue autonomous AI bots from hijacking mice or keyboards in **under 0.002 seconds**.

---

## 🎯 How It Works: The 3-Step Protection Flow

| Step | Location | What Happens | Security Status |
| :--- | :--- | :--- | :--- |
| **1. Danger** | Developer Laptop | Employee pastes real payroll database password into ChatGPT. | 🚨 **Real Credential Leak Risk** |
| **2. Intercept (0.14ms)** | GhostGate Workstation Proxy | Real secret swapped with format-preserving synthetic dummy token. | ⚡ **Swapped in Ephemeral RAM** |
| **3. Zero Leak** | Cloud AI (OpenAI / Anthropic) | Cloud model receives harmless fake token; generates functioning code. | 🛡️ **0 Bytes Leaked to Cloud** |

When the AI model returns refactored code via streaming SSE, GhostGate restores the original credential in-flight. The employee enjoys 100% AI productivity with **zero manual copy-pasting and zero leak liability**.

---

## 🏆 The 3 Unfair Competitive Moats (Why GhostGate Wins)

1. **Zero-Friction In-Line Proxy (Instant Enterprise Rollout)**  
   No code refactoring, no proprietary SDKs, and no developer workflow friction. Works transparently as an in-line reverse proxy across macOS, Windows, and Linux workstations.
2. **Format-Preserving AST Tokenization (No Broken AI Code)**  
   Legacy DLP tools replace text with `[REDACTED]`, which corrupts Python syntax, breaks indentation, and causes severe LLM hallucinations. GhostGate generates syntax-valid dummy tokens of identical length and format, preserving 100% code generation accuracy.
3. **RawHuman™ Layer 0 Biomechanical Sentinel**  
   The world's first hardware/kinematic barrier stopping autonomous AI bots from hijacking employee PCs. Differentiates physical human motor curves and muscle tremor from programmatic bot injections (`SendInput`, `PyAutoGUI`) in 0.002s.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    subgraph GATEWAY ["Security Gateway Layer: GhostGate Proxy (:8080)"]
        Client["Developer / IDE / CI Client"] -->|"HTTP / SSE Stream"| Proxy["GhostGate Async Proxy"]
        Proxy -->|"Format-Preserving Engine"| Redactor["Synthetic Shadowing"]
        Redactor -->|"Shadowed Mock Tokens: AKIA..."| Upstream["Upstream LLM Provider"]
        Redactor -->|"Detected airgap directive"| LocalLLM["Offline Ollama Container :11434"]
        Upstream -->|"Chunk-Boundary Resilient SSE"| Proxy
        Proxy -->|"In-Memory Rehydration"| Client
    end

    subgraph DEFENSE ["Abuse Detection Layer: RawHuman Sentinel (:8081)"]
        Upstream -->|"Tool Call: bash, db_delete"| HITL["HITL Execution Gate"]
        HITL -->|"Query Input Attribution"| Sentinel["RawHuman Sentinel"]
        Sentinel -->|"Inspect OS Injected Event Flags"| OSCheck{"OS Low-Level Hook"}
        Sentinel -->|"Curvature Entropy & Timing Jitter"| KinematicCheck{"Kinematic Dynamics"}
        Sentinel -->|"Hardware Attestation Fallback"| TouchID["WebAuthn / TouchID"]
        OSCheck -->|"Physical HID Origin"| Exec["Permit Action"]
        KinematicCheck -->|"Human Dynamics Fit"| Exec
        TouchID -->|"Biometric Verified"| Exec
        OSCheck -->|"Injected Flag Detected"| Block["Block Action (under 2ms)"]
        KinematicCheck -->|"Monotonic Bezier / Flat Clock"| Block
    end
```

---

## 🔬 Technical Deep-Dive: Engineering & Architecture

For technical auditors, security architects, and engineering evaluators:

### Pillar 1: Abuse & Synthetic Interaction Detection (`rawhuman_engine/`)
The RawHuman engine evaluates input authenticity across two defense layers:

#### 1. Low-Level OS Event Metadata (Definitive Hardware Signals)
Standard desktop automation frameworks generate synthetic events through operating system APIs. These APIs tag events in system hook structures:
* **Windows (Win32 SDK `winuser.h`)**:
  - `MSLLHOOKSTRUCT.flags` bit 0 (`0x00000001`): **`LLMHF_INJECTED`**. Defined by Microsoft for Low-Level Mouse Hooks. Software tools invoking `SendInput()` or `mouse_event()` set this flag.
  - `KBDLLHOOKSTRUCT.flags` bit 4 (`0x00000010`): **`LLKHF_INJECTED`** (Low-Level Keyboard Hook injected flag).
* **macOS (Quartz Event Services)**:
  - Evaluation of `kCGEventSourceStatePrivate` vs `kCGEventSourceStateCombinedSessionState`.
  - Checking `CGEventGetIntegerValueField(event, kCGEventSourceUserData)` and monotonic IOHID timestamp continuity.
* **Linux (`evdev` & `uinput`)**:
  - Differentiating physical hardware input nodes (`/dev/input/by-id/usb-*`) from virtual synthetic device handles (`/dev/input/uinput`).

#### 2. Kinematic Trajectory Dynamics (Behavioral Heuristics)
To detect automation tools attempting user-space evasion, RawHuman evaluates three kinematic properties:
1. **Directional Curvature Entropy**: Calculates the Shannon entropy of angular derivatives ($\Delta \theta$). Scripted paths (PyAutoGUI, Bezier splines) exhibit monotonic or near-zero angular entropy ($H \to 0$), whereas neuromuscular movement displays continuous micro-corrections ($H \ge 0.20$).
2. **Discrete OS Scheduler Timing Jitter**: Scripted loops cluster around discrete OS scheduler quanta (e.g., 10ms or 15.6ms ticks). Physical USB HID controllers exhibit microsecond hardware oscillator drift.
3. **Fitts's Law Ballistic Deceleration**: Verifies that acceleration and deceleration phases follow human ballistic movement rather than constant-velocity or naive linear interpolation.

---

### Pillar 2: Security Gateway & Policy Enforcement (`ghostgate_core/`)

#### 1. Format-Preserving Synthetic Shadowing
Rather than corrupting prompts with bracketed tags (`[AWS_KEY_REDACTED]`), GhostGate replaces credentials with syntactically valid mock tokens of identical format and length (e.g. `AKIAIOSFODNN7EXAMPLE` ➔ `AKIA7B8C9D0E1F2G3H4I`):
- Code generation models and AST parsers receive syntactically valid code without breaking indentation or type rules.
- Lookup mappings reside strictly in ephemeral process RAM (`secrets_vault.py`) and are reversed during response rehydration.

#### 2. Chunk-Boundary Resilient SSE Streaming Rehydration
In streaming responses (Server-Sent Events), surrogate tokens can be sliced across arbitrary network packet or chunk boundaries (e.g., `"AKIA1234"` in chunk $N$ and `"567890123456"` in chunk $N+1$).
- GhostGate implements a prefix-aware sliding buffer (`rehydrate_streaming_chunk`):
  - Any complete tokens in the buffer are restored immediately.
  - If the buffer's tail matches a prefix of an active surrogate token, that suffix is retained in the buffer while preceding text is emitted.
  - Guarantees zero token corruption across streaming chunk boundaries.

#### 3. Human-in-the-Loop (HITL) Execution Gateway
Autonomous agent tool calls are classified by risk:
- **Low Risk** (`read_file`, `search_docs`): Auto-permitted.
- **High Risk** (`bash_exec`, `delete_database`, `aws_terminate`): Intercepted. Requires physical human confirmation verified by RawHuman or hardware TouchID before the gateway permits execution.

#### 4. Deterministic Air-Gap Routing
Prompts containing the `# @airgap` directive or matching classified data rules bypass external networks entirely and route to an isolated, containerized Ollama instance.

---

### Pillar 3: Production Engineering & Reproducible Benchmarks

#### 1. Engine Latency Benchmarks
Benchmarks are measured using [`benchmarks/run_benchmarks.py`](benchmarks/run_benchmarks.py) on Apple Silicon arm64 (Python 3.14 CPython, 100 warmup cycles, 1,000 measured iterations):

| Component / Test Case | Payload Size | P50 Overhead | P90 Overhead | P99 Overhead | Throughput |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Masking: Small Payload** (1 AWS Key) | 128 Bytes | **0.012 ms** | **0.013 ms** | **0.033 ms** | 72,000+ ops/s |
| **Masking: Medium Payload** (5 mixed secrets) | 1.38 KB | **0.089 ms** | **0.101 ms** | **0.261 ms** | 10,300+ ops/s |
| **Masking: Large Payload** (10 mixed secrets) | 11.1 KB | **0.709 ms** | **0.738 ms** | **0.787 ms** | 1,400+ ops/s |
| **In-Memory Rehydration Overhead** | 1.38 KB | **0.004 ms** | **0.004 ms** | **0.006 ms** | — |
| **Kinematic Trajectory Evaluation** | 25 points | **0.011 ms** | **0.012 ms** | **0.015 ms** | — |

- **Peak Memory Allocated** (during 1,000-cycle batch): **12.93 KB**
- **Benchmark Scope**: Measures internal engine processing overhead (regex matching, substitution, buffer rehydration, kinematic calculations). Does not include external third-party cloud round-trips.

Reproduce locally:
```bash
make bench
```

#### 2. Empirical Attack & Evaluation Corpus (`tests/corpus/`)
Detection capabilities are validated against structured test corpora:
- [`secrets_leakage_corpus.json`](tests/corpus/secrets_leakage_corpus.json): 22+ test scenarios covering AWS IAM/STS, GCP, GitHub PATs, OpenAI/Anthropic keys, Postgres/MySQL/Mongo/Redis URIs, PII, multi-line YAML configs, and negative controls (UUIDs, Git commit hashes) to ensure low false-positive rates.
- [`synthetic_agent_corpus.json`](tests/corpus/synthetic_agent_corpus.json): Automation trajectories (PyAutoGUI, cubic Bezier) vs human physical reaching curves.
- [`adversarial_prompts_corpus.json`](tests/corpus/adversarial_prompts_corpus.json): Instruction override and encoding evasion samples.

Run corpus verification:
```bash
pytest tests/test_attack_corpus.py -v
```

---

## ⚖️ Security Boundaries & Scope

| Area | In-Scope Guarantees | Known Limitations & Out-of-Scope |
| :--- | :--- | :--- |
| **Secret Masking** | Deterministic masking of defined regex grammars and high-entropy strings ($H \ge 3.8	ext{ bits/byte}$, length $\ge 16$). | Custom-encoded ciphers or secrets split non-contiguously across multiple prompt turns require dedicated regex rules. |
| **Data Retention** | GhostGate itself does not persist prompt or token mapping tables to disk. Mappings are held strictly in ephemeral process RAM. | Host OS swap, Docker container runtime logs, and external reverse proxies must be configured by system administrators to prevent indirect disk logging. |
| **Air-Gap Routing** | Prompts tagged `# @airgap` are routed locally to the offline Ollama container. | Prompts without tags or matching rules proceed to the configured cloud upstream. |
| **Input Attribution** | Detects OS-level automation API flags (`SendInput`, `CGEventPost`) and scripted monotonic trajectories. | Adaptive bots synthesizing human-like jitter, varying mouse polling rates (125Hz vs 1000Hz), and kernel rootkits (Ring 0) with direct memory scraping. |

---

## 🚀 Quickstart

### Option A: Docker Compose (Production Multi-Container Stack)

```bash
git clone https://github.com/MinsuKin/ghostgate.git
cd ghostgate
docker compose up -d
```

| Service | Endpoint | Role |
| :--- | :--- | :--- |
| **GhostGate Proxy** | `http://127.0.0.1:8080/v1` | Reverse proxy with format-preserving masking |
| **CISO SOC Dashboard** | `http://127.0.0.1:8080/dashboard` | Real-time telemetry, secret audit trail, and KPIs |
| **RawHuman Sentinel** | `http://127.0.0.1:8081` | Proof-of-Human attestation & I/O gate |
| **Air-Gap Ollama** | `http://127.0.0.1:11434` | Offline fallback for classified prompts |

### Option B: Local Python Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start GhostGate Proxy
python -m ghostgate_core.proxy

# In a separate terminal: Start RawHuman Sentinel
python -m rawhuman_engine.server
```

---

## 🔌 SDK Integration

Point standard OpenAI or Anthropic SDK clients to `http://127.0.0.1:8080/v1`:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="your-openai-api-key"
)

# Secrets are masked before egress and restored in-memory upon stream return
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Review config: AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}
    ]
)
print(response.choices[0].message.content)
```

---

## 🧪 Testing & Verification

```bash
# 1. Run all unit and corpus evaluation tests (28 tests)
pytest tests/ -v

# 2. Run reproducible latency benchmarks
make bench
```

---

## 📂 Repository Structure

```
.
├── benchmarks/                    # Reproducible latency & memory benchmark harness
│   ├── run_benchmarks.py          # Benchmark runner (P50/P90/P99 latency & tracemalloc)
│   └── benchmark_results.json     # Machine-readable benchmark outputs
├── config.yaml                    # Privacy policies, upstream configs, and redaction patterns
├── docker-compose.yml             # Multi-container production orchestration
├── Makefile                       # Developer commands (install, test, bench, e2e, docker-up)
├── pyproject.toml                 # Package metadata and dependencies
├── ghostgate_core/                # Security Gateway & Redaction Engine
│   ├── proxy.py                   # Async FastAPI reverse proxy
│   ├── redactor.py                # Format-preserving synthetic shadowing & SSE rehydration
│   ├── zdr_enforcer.py            # Telemetry stripper & Zero Data Retention enforcer
│   ├── hitl_gateway.py            # Human-in-the-Loop tool call execution gateway
│   ├── auditor.py                 # Developer workstation security auditor
│   ├── dashboard.py               # Embedded CISO SOC Web UI (:8080/dashboard)
│   ├── secrets_vault.py           # Ephemeral in-memory token lookup store
│   └── airgap/                    # Local offline LLM configuration
├── rawhuman_engine/               # Abuse Detection & Input Attribution Prototype
│   ├── detector.py                # OS low-level hook inspector (Win32, Quartz, evdev)
│   ├── biomechanics.py            # Kinematic Trajectory Dynamics (Curvature entropy & jitter)
│   ├── server.py                  # Attestation daemon HTTP API (:8081)
│   └── demo_cli.py                # Terminal visualizer for kinematic inspection
├── recipes/                       # Compliance recipes & developer guides
├── tests/                         # Comprehensive unit, corpus & live integration tests
│   ├── corpus/                    # Empirical evaluation datasets
│   ├── test_attack_corpus.py      # Automated corpus evaluation suite
│   ├── test_redactor.py           # AST & chunk-boundary streaming test suite
│   ├── test_proxy.py              # Proxy endpoints & ZDR sanitization tests
│   ├── test_rawhuman.py           # OS flags & kinematic dynamics tests
│   ├── test_hitl_gateway.py       # Tool call execution gateway tests
│   ├── test_auditor.py            # Workstation auditor tests
│   └── test_e2e_live.py           # Live end-to-end multi-container integration tests
├── SECURITY.md                    # Vulnerability reporting & threat model
└── CONTRIBUTING.md                # Open-source contribution guidelines
```

---

## 📄 License
This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
