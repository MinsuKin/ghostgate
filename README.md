<p align="center">
  <h1 align="center">🛡️ RAWHUMAN <small>by GhostGate</small></h1>
  <p align="center">
    <strong>The First I/O-Level Defense Against Multimodal Autonomous AI Agents</strong><br>
    <em>CAPTCHA is Dead in the Browser • Layer 0 Hardware & Kinematic Attestation • HITL Secure Execution Gateway</em>
  </p>
  <p align="center">
    <a href="https://ghostgate-beta.vercel.app/" target="_blank"><img src="https://img.shields.io/badge/LIVE%20DEMO-ghostgate--beta.vercel.app-6366F1?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Interactive Sandbox"></a>
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
    <img src="https://img.shields.io/badge/python-3.10%2B-brightgreen.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/docker-ready-2496ED.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/tests-28%20passed-success.svg" alt="Tests: 28 passed">
    <img src="https://img.shields.io/badge/layer0%20lockout-%3C0.002s-rose.svg" alt="Lockout: <0.002s">
    <img src="https://img.shields.io/badge/format--preserving-%3C0.15ms-indigo.svg" alt="Latency: <0.15ms">
  </p>
</p>

---

> ### 🌐 Live Interactive Sandbox (No Install Required)
> **Experience the Layer 0 Agent Defense live in your browser:**  
> 👉 **[https://ghostgate-beta.vercel.app/](https://ghostgate-beta.vercel.app/)**  
> Test real-world rogue autonomous AI agent hijack simulations (SendInput bot vs physical human mouse) with live 0.002s lockout dials, and explore downstream 0.14ms format-preserving secret shadowing.

---

## 🧭 Executive Summary: Why CAPTCHA is Dead

### 1. The Death of Web CAPTCHA
For twenty years, online bot protection (Google reCAPTCHA v2/v3, Cloudflare Turnstile) relied on code running inside the **browser's JavaScript DOM sandbox**—tracking DOM `mousemove` events, canvas fingerprints, and rendering challenge puzzles.

**Autonomous multimodal AI agents (Anthropic Claude 3.5 Computer Use, OpenAI Operator) broke this paradigm permanently:**
* **Direct Desktop Pixel Inspection**: AI agents don't parse web DOM; they inspect the workstation's raw screen pixels via multimodal vision.
* **OS-Level Input Injection**: Instead of dispatching JavaScript events, agents inject native operating system input interrupts (`SendInput` on Windows, Quartz Event Taps on macOS, `uinput` on Linux).
* **DOM Blindness**: To browser JavaScript, these inputs appear indistinguishable from human activity, or the agent operates entirely outside the browser (in native terminal shells, IDEs, desktop databases).
* **The Emerging Threat**: If a rogue agent is tricked by a prompt injection attack, it can physically click "Approve Transfer" or delete production databases with zero human oversight.

### 2. The Solution: RawHuman + GhostGate Architecture
True proof-of-human can no longer exist at the application or web layer. **It must happen at Layer 0 (the OS Kernel and physical I/O interface):**

1. 🛡️ **RawHuman™ Layer 0 Sentinel**: Traps OS programmatic injection flags (`LLMHF_INJECTED = 0x01`), inspects physical USB HID controller hardware interrupts, and validates biological neuromuscular curvature entropy ($H \ge 0.20$) in **under 0.002 seconds**. Programmatic bot clicks are neutralized before they execute.
2. ⚡ **GhostGate™ Secure HITL Execution Gateway**: Once human authenticity is attested at Layer 0, GhostGate intercepts high-risk tool calls (`bash`, `db_drop`) and performs **0.14ms format-preserving secret shadowing**, ensuring corporate credentials never leak to cloud LLMs.
3. 🔄 **Lossless In-Memory Rehydration**: Restores authentic credentials in ephemeral memory on the developer's laptop, preserving 100% LLM coding productivity with zero leak risk.

---

## 🎯 How It Works: The Layer 0 Protection Flow

| Step | Location | What Happens | Security Status |
| :--- | :--- | :--- | :--- |
| **1. Agent Action** | Workstation OS | Autonomous AI agent attempts mouse click / tool execution via `SendInput`. | 🚨 **Autonomous Bot Takeover Risk** |
| **2. Layer 0 Trap (0.002s)** | RawHuman Engine | Detects OS injection flag (`LLMHF_INJECTED`) & flat non-tremor trajectory ($H < 0.20$). | ⚡ **I/O Bus Locked in 0.002s** |
| **3. Secure Gateway** | GhostGate Proxy | Verified human actions proceed; secrets shadowed with format-preserving mock tokens. | 🛡️ **Zero Breach & Zero LLM Leak** |

---

## 🏆 The 3 Unfair Competitive Moats (Why RawHuman Wins)

1. **Layer 0 Hardware & OS Kernel Moat (The reCAPTCHA Killer)**  
   Operates where browser JavaScript sandboxes cannot reach. Intercepts Win32 low-level hooks, macOS Quartz session state, and Linux physical `evdev` bus descriptors before synthetic inputs reach the application layer.
2. **Neuromuscular Kinematic Biomechanics ($H \ge 0.20$)**  
   Biological human hand motion strictly follows Fitts's Law, minimum-jerk curves, and micro-tremor timing jitter. Programmatic bots generate piecewise linear paths with discrete OS scheduler timing intervals, creating a deterministic mathematical separation.
3. **In-Line HITL Execution & Format-Preserving Data Shield**  
   Unlike dumb DLP filters that replace text with `[REDACTED]` (breaking code AST and hallucinating LLMs), GhostGate generates syntax-valid dummy tokens in 0.14ms with zero data retention (ZDR).

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
