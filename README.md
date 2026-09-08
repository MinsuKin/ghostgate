<p align="center">
  <h1 align="center">🛡️ GHOSTGATE</h1>
  <p align="center">
    <strong>Open-Source AI Privacy Proxy & Agentic I/O Sentinel for Enterprise LLM Workflows</strong><br>
    <em>Format-Preserving Data Sovereignty • Zero Disk Retention • Kinematic Proof-of-Human Sentinel</em>
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
    <img src="https://img.shields.io/badge/python-3.10%2B-brightgreen.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/docker-ready-2496ED.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/tests-26%20passed-success.svg" alt="Tests: 26 passed">
    <img src="https://img.shields.io/badge/benchmark-reproducible-blue.svg" alt="Benchmark: Reproducible">
    <img src="https://img.shields.io/badge/attack%20corpus-validated-brightgreen.svg" alt="Attack Corpus Validated">
  </p>
</p>

---

## ⚡ The Dual Security Challenge in Modern AI

As software teams integrate commercial LLMs and autonomous agents into developer workstations, standard enterprise perimeters face two critical vulnerabilities:

1. **Outbound Data Exfiltration**: Commercial LLM APIs retain prompts in plaintext for **30 to 90 days** for safety reviews and potential fine-tuning. When developers paste code containing API keys, private keys, database connection strings, or customer PII, secrets are broadcast to third-party logs. Naive redaction (e.g., `[REDACTED_SECRET]`) breaks code syntax, regex validation, and LLM reasoning.
2. **Inbound Agent Takeover & Synthetic I/O Hijacking**: Multimodal autonomous desktop agents (e.g. Anthropic Computer Use, OpenAI Operator) capture desktop frames and issue programmatic OS input events (`SendInput`, `CGEventPost`, `uinput`). Standard browser-level protections (`event.isTrusted`) are bypassed at the operating system layer.

**GhostGate** provides a lightweight, local security proxy and I/O sentinel that addresses both vectors locally without requiring proprietary cloud middleware.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    subgraph OUTBOUND ["1. Outbound Protection: GhostGate Privacy Proxy (:8080)"]
        Dev[Engineer / IDE / CI Pipeline] -->|Prompt with Secrets & Code| Proxy[GhostGate Proxy :8080]
        Proxy -->|Format-Preserving AST Engine| Redactor[Synthetic Shadowing Engine]
        Redactor -->|Valid Mock Tokens: AKIA... 20 chars| CloudLLM[Commercial Cloud LLM Provider]
        Redactor -->|Detected #@airgap tag| LocalLLM[Offline Air-Gap Ollama Container :11434]
        CloudLLM -->|Streamed SSE Response| Proxy
        Proxy -->|In-Memory Rehydration| Dev
    end

    subgraph INBOUND ["2. Inbound Protection: RawHuman Sentinel (:8081)"]
        CloudLLM -->|Autonomous Tool Call: bash, db_delete| Gateway[HITL Execution Gateway]
        Gateway -->|Halt & Request Physical Presence| Sentinel[RawHuman Sentinel]
        Sentinel -->|Inspect OS Injected Event Flags| OSCheck{OS Low-Level Hook Check}
        Sentinel -->|Directional Curvature Entropy & Jitter| KinematicCheck{Kinematic Trajectory}
        Sentinel -->|ADA / Sensor Fallback| TouchID[Hardware TouchID / WebAuthn]
        OSCheck -->|Physical HID Origin| Exec[Execute Tool Call]
        KinematicCheck -->|Ballistic Jitter Confirmed| Exec
        TouchID -->|Biometric Verified| Exec
        OSCheck -->|Flag Detected: Synthetic Injected| Block[Terminate Action (< 2ms)]
        KinematicCheck -->|Flat Jitter / Synthetic Bezier| Block
    end
```

---

## 🔬 Systems Architecture & Detection Specifications

### 1. Format-Preserving Synthetic Shadowing
Rather than corrupting prompts with bracketed tags (`[AWS_KEY_REDACTED]`), GhostGate uses **format-preserving synthetic shadowing**:
- Detected secrets are mapped to syntactically indistinguishable mock values conforming to the exact regex pattern, length, and character alphabet (e.g., an AWS key `AKIAIOSFODNN7EXAMPLE` is shadowed as `AKIA7B8C9D0E1F2G3H4I`).
- Downstream LLM code generation and syntax parsers (AST) treat the mock value as valid code without syntax errors.
- Translations are preserved in ephemeral process memory (`secrets_vault.py`) and reversed in real-time across both unary JSON and streaming Server-Sent Events (SSE). **Zero tokens or prompts are ever written to disk.**

### 2. OS-Level Synthetic Event Flag Inspection
To detect programmatic injection without relying on browser heuristics, the RawHuman engine inspects low-level OS event pipeline flags:

* **Windows (Win32 SDK `winuser.h`)**:
  - `MSLLHOOKSTRUCT.flags` bit 0 (`0x00000001`): **`LLMHF_INJECTED`**. *Note: `LLMH` stands for **Low-Level Mouse Hook**, defined by Microsoft in Windows 2000 (`winuser.h`) — it is an OS subsystem flag, not an AI buzzword.*
  - `KBDLLHOOKSTRUCT.flags` bit 4 (`0x00000010`): **`LLKHF_INJECTED`** (Low-Level Keyboard Hook injected flag).
  - Software automation tools calling `SendInput()` or `mouse_event()` automatically trigger these flags unless kernel drivers are modified.
* **macOS (Quartz Event Services)**:
  - Evaluation of `kCGEventSourceStatePrivate` vs `kCGEventSourceStateCombinedSessionState`.
  - Inspection of `CGEventGetIntegerValueField(event, kCGEventSourceUserData)` and monotonic IOHID timestamp continuity.
* **Linux (evdev & uinput)**:
  - Inspection of input device sysfs nodes, isolating physical USB HID endpoints (`/dev/input/by-id/usb-*`) from virtual synthetic device handles (`/dev/input/uinput`).

### 3. Kinematic Trajectory Dynamics
Early academic concepts suggested measuring human hand tremor (8–12Hz) via mouse coordinate sampling. In production environments, OS scheduler timer quantization, mouse sensor polling rates (125Hz–1000Hz), and vendor micro-smoothing render frequency-domain biological tremor detection mathematically unreliable in user space.

GhostGate instead enforces **Kinematic Trajectory Dynamics**:
1. **Directional Curvature Entropy**: Calculation of the Shannon entropy of directional change angles ($\Delta \theta$). Robotic trajectories exhibit monotonic Bezier curvatures ($H \to 0$), whereas neuromuscular movements display continuous non-zero angular entropy ($H \ge 0.20$).
2. **Discrete OS Scheduler Timing Jitter**: Measurement of inter-event timing variance relative to hardware interrupt intervals ($J = |(t_{i+1} - t_i) - \overline{\Delta t}| / \overline{\Delta t}$). Scripted bots emit uniform delay quantums ($\sigma \approx 0$).
3. **Fitts's Law Ballistic Deceleration**: Validation that acceleration and deceleration phases match human ballistic reaching laws rather than constant-velocity or naive easing algorithms.

---

## 🎯 Empirical Attack & Evaluation Corpus (`tests/corpus/`)

To prevent regression and evaluate detection efficacy against real-world attack vectors, GhostGate maintains a structured evaluation corpus in [`tests/corpus/`](tests/corpus/):

* **[`secrets_leakage_corpus.json`](tests/corpus/secrets_leakage_corpus.json)**:
  - 22+ curated test cases spanning cloud provider credentials (AWS IAM/STS, GCP), developer tokens (GitHub classic & fine-grained PATs), LLM keys (OpenAI legacy & project, Anthropic), database connection strings (Postgres, MySQL, Mongo, Redis), PII (emails, IPs, phone numbers), complex multi-line YAML configs, and negative controls (UUIDs, Git commit hashes, normal high-vocabulary English).
* **[`synthetic_agent_corpus.json`](tests/corpus/synthetic_agent_corpus.json)**:
  - Mouse trajectories from PyAutoGUI linear interpolation, monotonic cubic Bezier curves, and physical human reaching movements.
* **[`adversarial_prompts_corpus.json`](tests/corpus/adversarial_prompts_corpus.json)**:
  - Adversarial prompt injection samples attempting instruction overrides, base64 evasion, and markdown code fence extraction.

Run the automated corpus evaluation:
```bash
pytest tests/test_attack_corpus.py -v
```

---

## 📊 Reproducible Latency Benchmarks & Profiling

### Benchmark Methodology
Benchmarks are measured using the automated harness in [`benchmarks/run_benchmarks.py`](benchmarks/run_benchmarks.py).
- **Environment**: Apple Silicon arm64, Darwin 25.6.0, Python 3.14 (CPython).
- **Protocol**: Single-thread synchronous execution, 100 warmup iterations followed by 1,000 measured iterations per test.
- **Memory Profiling**: Measured using Python `tracemalloc` for peak memory allocation during batch operations.

### Empirical Results

| Test Case | Payload Size | P50 Latency | P90 Latency | P99 Latency | Throughput |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Small Payload Masking** (1 AWS Key) | 128 Bytes | **0.013 ms** | **0.013 ms** | **0.016 ms** | 78,000+ ops/sec |
| **Medium Payload Masking** (5 mixed secrets) | 1.38 KB | **0.088 ms** | **0.101 ms** | **0.285 ms** | 10,100+ ops/sec |
| **Large Payload Masking** (10 mixed secrets) | 11.1 KB | **0.693 ms** | **0.728 ms** | **0.940 ms** | 1,400+ ops/sec |
| **In-Memory Rehydration Overhead** | 1.38 KB | **0.004 ms** | **0.004 ms** | **0.004 ms** | — |
| **Kinematic Trajectory Evaluation** | 25 points | **0.011 ms** | **0.012 ms** | **0.015 ms** | — |

- **Peak Heap Memory Allocated** (during 1,000-cycle batch): **12.89 KB**
- **Disk Persistence**: **0 bytes** (All translation dictionaries are RAM-only and ephemeral).

To reproduce these benchmarks on your machine:
```bash
make bench
```

---

## ⚖️ Security Scope & Known Boundaries

In production security engineering, no tool provides absolute protection. GhostGate explicitly defines its detection boundaries and known trade-offs:

| Layer | What GhostGate Protects | Known Limitations & Trade-offs |
| :--- | :--- | :--- |
| **Secret Masking** | Deterministic detection & format-preserving masking of defined regex grammars (AWS, GCP, GitHub, Slack, OpenAI, Anthropic, DB URIs, PII) and high-entropy strings ($H \ge 3.8\text{ bits/byte}$, length $\ge 16$). | Custom-encoded secrets (e.g. base64-within-hex, rot13) or secrets broken across multiple non-contiguous prompts require custom regex definitions. |
| **Entropy Engine** | High-entropy random strings without predefined regex formats (e.g. proprietary tokens). | Natural high-entropy strings (e.g., base64 media headers, scientific constants) may trigger false positives unless excluded by custom rules. |
| **Data Retention** | Ephemeral RAM storage. Zero tokens, prompts, or mapping dictionaries are written to persistent disk. | Process memory can be inspected if an attacker possesses root/administrator privileges and attaches a debugger (`ptrace`/`lldb`). |
| **Air-Gap Routing** | Deterministic local diversion to offline Ollama container when prompted with `# @airgap` or configured sensitive patterns. | Requires local Docker daemon and Ollama service running. Prompts without the tag/pattern proceed to the configured cloud upstream. |
| **Kinematic Sentinel** | Programmatic automation tools using standard OS user-space APIs (`SendInput`, `CGEventPost`, `uinput`) and robotic Bezier/linear mouse movements. | High-polling gaming mice (1000Hz+) vs office mice (125Hz) have different jitter profiles; assistive trackpad smoothing may require TouchID/WebAuthn fallback. |
| **Host Integrity** | User-space process boundaries. | Out of scope: Kernel rootkits (Ring 0) and physical USB hardware implants (e.g. custom microcontroller emulating USB HID hardware interrupts). |

---

## ⚡ Quickstart

### Option A: Docker Compose (Production Multi-Container Stack)

Launch the full stack (GhostGate Proxy, RawHuman Sentinel, and Offline Air-Gap Ollama container) in one command:

```bash
git clone https://github.com/MinsuKin/ghostgate.git
cd ghostgate
docker compose up -d
```

| Service | Endpoint | Purpose |
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

# Run GhostGate Proxy
python -m ghostgate_core.proxy

# In a separate terminal: Run RawHuman Sentinel
python -m rawhuman_engine.server
```

---

## 🔌 Drop-In SDK Integration

Point your existing OpenAI or Anthropic SDK clients to `http://127.0.0.1:8080/v1`:

### Python (OpenAI SDK)
```python
from openai import OpenAI

# GhostGate intercepts, shadows secrets, strips telemetry, and rehydrates responses
client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="your-openai-api-key"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Review this config: AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}
    ]
)

# Response is automatically rehydrated in memory
print(response.choices[0].message.content)
```

### Deterministic Air-Gap Routing
Tag any prompt with `# @airgap` to prevent external network egress. GhostGate diverts the prompt to the local offline Ollama container:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "# @airgap Analyze our internal merger agreement..."}
    ]
)
# Handled 100% locally via Ollama — zero bytes leave the workstation.
```

---

## 🛠️ Workstation Security Tools

### Workstation AI Security Auditor (`ghostgate audit`)
Inspect local developer workstations (Cursor IDE, VS Code, shell environments) for unencrypted keys and telemetry leakage:

```bash
python -m ghostgate_core.cli audit
```

### RawHuman Interactive Verification Demo
Simulate live autonomous agent input injection vs authentic biological mouse motion:

```bash
python -m rawhuman_engine.demo_cli
```

---

## 📂 Repository Structure

```
.
├── benchmarks/                    # Reproducible latency & memory benchmark harness
│   ├── run_benchmarks.py          # Benchmark runner (P50/P90/P99 latency & tracemalloc)
│   └── benchmark_results.json     # Machine-readable benchmark outputs
├── config.yaml                    # Privacy policies, upstream configs, and redaction patterns
├── docker-compose.yml             # Production multi-container orchestration
├── Makefile                       # Developer shortcuts (build, run, test, bench, e2e)
├── pyproject.toml                 # Package metadata and dependencies
├── ghostgate_core/                # Layer 7 Privacy Proxy & Redaction Engine
│   ├── proxy.py                   # Async FastAPI reverse proxy
│   ├── redactor.py                # Format-preserving synthetic shadowing engine
│   ├── zdr_enforcer.py            # Telemetry stripper & Zero Data Retention enforcer
│   ├── hitl_gateway.py            # Human-in-the-Loop tool call execution gateway
│   ├── auditor.py                 # Developer workstation security auditor
│   ├── dashboard.py               # Real-time CISO SOC Web UI (:8080/dashboard)
│   ├── secrets_vault.py           # Ephemeral in-memory token lookup store
│   └── airgap/                    # Local offline LLM configuration
├── rawhuman_engine/               # Layer 0 / I/O Proof-of-Human Sentinel
│   ├── detector.py                # OS low-level hook inspector (Win32, Quartz, evdev)
│   ├── biomechanics.py            # Kinematic Trajectory Dynamics (Curvature entropy & jitter)
│   ├── server.py                  # Attestation daemon HTTP API (:8081)
│   └── demo_cli.py                # Terminal visualizer for kinematic inspection
├── recipes/                       # Audit-ready compliance recipes
│   ├── RECIPE_MATRIX.md           # Configuration recipes for OpenAI, Anthropic, Cursor, etc.
│   ├── enterprise_compliance.md   # Legal DPA addendum & Data Sovereignty policy
│   └── developer_cheatsheet.md    # Developer setup cheat sheet
├── tests/                         # Comprehensive unit, corpus & live integration tests
│   ├── corpus/                    # Empirical evaluation datasets
│   │   ├── secrets_leakage_corpus.json  # 22+ categorized secret leak test cases
│   │   ├── synthetic_agent_corpus.json  # Agent vs human trajectory datasets
│   │   └── adversarial_prompts_corpus.json # Adversarial evasion prompts
│   ├── test_attack_corpus.py      # Automated corpus evaluation suite
│   ├── test_redactor.py           # AST & format-preserving test suite
│   ├── test_proxy.py              # Proxy endpoints & ZDR sanitization tests
│   ├── test_rawhuman.py           # OS flags & kinematic dynamics tests
│   ├── test_hitl_gateway.py       # Tool call execution gateway tests
│   ├── test_auditor.py            # Workstation auditor tests
│   └── test_e2e_live.py           # Live end-to-end multi-container integration tests
├── SECURITY.md                    # Vulnerability reporting & threat model
└── CONTRIBUTING.md                # Open-source contribution guidelines
```

---

## 🧪 Testing & Verification

Run the full automated test and benchmark suites locally:

```bash
# 1. Run unit and corpus evaluation tests (21 tests)
pytest tests/ -v -k "not e2e"

# 2. Run live container E2E integration tests (5 tests)
pytest tests/test_e2e_live.py -v -s

# 3. Execute latency & memory benchmark suite
make bench
```

---

## 🤝 Community & Security Governance

- **Security Advisories & Threat Model**: See [SECURITY.md](SECURITY.md).
- **Contributing Guidelines**: See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Compliance & Legal Addenda**: See [recipes/enterprise_compliance.md](recipes/enterprise_compliance.md).

## 📄 License
This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
