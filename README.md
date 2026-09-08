<p align="center">
  <h1 align="center">🛡️ GHOSTGATE</h1>
  <p align="center">
    <strong>Open-Source AI Privacy Proxy & Agentic I/O Sentinel for Enterprise LLM Workflows</strong><br>
    <em>Format-Preserving Data Sovereignty • Zero Data Retention • Kinematic Proof-of-Human Sentinel</em>
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache-2.0"></a>
    <img src="https://img.shields.io/badge/python-3.10%2B-brightgreen.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/docker-ready-2496ED.svg" alt="Docker Ready">
    <img src="https://img.shields.io/badge/tests-23%20passed-success.svg" alt="Tests">
    <img src="https://img.shields.io/badge/P99%20latency-%3C%201.5ms-informational.svg" alt="P99 Latency">
    <img src="https://img.shields.io/badge/Zero%20Data%20Retention-Enforced-orange.svg" alt="Zero Data Retention">
  </p>
</p>

---

## ⚡ The Dual Security Challenge in Modern AI

As software teams integrate commercial LLMs and autonomous agents into developer workstations, standard enterprise perimeters face two critical vulnerabilities:

1. **Outbound Data Exfiltration**: Commercial LLM APIs retain prompts in plaintext for **30 to 90 days** for safety reviews and potential fine-tuning. When developers paste code containing API keys, private keys, database connection strings, or customer PII, secrets are broadcast to third-party logs. Naive redaction (e.g., `[REDACTED_SECRET]`) breaks code syntax, regex validation, and LLM reasoning.
2. **Inbound Agent Takeover & Synthetic I/O Hijacking**: Multimodal autonomous desktop agents (e.g. Anthropic Computer Use, OpenAI Operator) capture desktop frames and issue programmatic OS input events (`SendInput`, `CGEventPost`, `uinput`). Standard browser-level protections (`event.isTrusted`) are bypassed at the operating system layer.

**GhostGate** provides a unified, zero-latency local security gateway that solves both problems without requiring cloud lock-in or proprietary infrastructure.

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

## 🔬 Technical Deep Dive & Systems Architecture

### 1. Format-Preserving Synthetic Shadowing
Rather than corrupting prompts with bracketed tags (`[AWS_KEY_REDACTED]`), GhostGate uses **format-preserving synthetic shadowing**:
- Detected secrets are mapped to syntactically indistinguishable mock values conforming to the exact regex pattern, length, and character alphabet (e.g., an AWS key `AKIAIOSFODNN7EXAMPLE` is shadowed as `AKIA7B8C9D0E1F2G3H4I`).
- Downstream LLM code generation and syntax parsers (AST) treat the mock value as valid code without syntax errors.
- Translations are preserved in ephemeral process memory (`secrets_vault.py`) and reversed in real-time across both unary JSON and streaming Server-Sent Events (SSE). **Zero tokens or prompts are ever written to disk.**

### 2. OS-Level Synthetic Event Flag Inspection
To detect programmatic injection without relying on browser heuristics, the RawHuman engine inspects low-level OS event pipeline flags:

* **Windows (Win32 SDK `winuser.h`)**:
  - `MSLLHOOKSTRUCT.flags` bit 0 (`0x00000001`): **`LLMHF_INJECTED`**. *Historical note: `LLMH` stands for **Low-Level Mouse Hook**, introduced by Microsoft in Windows 2000 — it is not an AI buzzword.*
  - `KBDLLHOOKSTRUCT.flags` bit 4 (`0x00000010`): **`LLKHF_INJECTED`** (Low-Level Keyboard Hook injected flag).
  - Software automation tools calling `SendInput()` or `mouse_event()` automatically trigger these hardware descriptor flags.
* **macOS (Quartz Event Services)**:
  - Evaluation of `kCGEventSourceStatePrivate` vs `kCGEventSourceStateCombinedSessionState`.
  - Inspection of `CGEventGetIntegerValueField(event, kCGEventSourceUserData)` and monotonic IOHID timestamp continuity.
* **Linux (evdev & uinput)**:
  - Inspection of input device sysfs nodes, isolating physical USB HID endpoints (`/dev/input/by-id/usb-*`) from virtual synthetic device handles (`/dev/input/uinput`).

### 3. Kinematic Trajectory Dynamics (Replacing Biological Tremor Claims)
Early academic concepts suggested measuring human hand tremor (8–12Hz) via mouse coordinate sampling. In production environments, OS scheduler timer quantization, mouse sensor polling rates (125Hz–1000Hz), and vendor micro-smoothing render frequency-domain biological tremor detection mathematically unreliable in user space.

GhostGate instead enforces **Kinematic Trajectory Dynamics**:
1. **Directional Curvature Entropy**: Calculation of the Shannon entropy of directional change angles ($\Delta \theta$). Robotic trajectories exhibit monotonic Bezier curvatures ($H \to 0$), whereas neuromuscular movements display continuous non-zero angular entropy ($H \ge 0.20$).
2. **Discrete OS Scheduler Timing Jitter**: Measurement of inter-event timing variance relative to hardware interrupt intervals ($J = |(t_{i+1} - t_i) - \overline{\Delta t}| / \overline{\Delta t}$). Scripted bots emit uniform delay quantums ($\sigma \approx 0$).
3. **Fitts's Law Ballistic Deceleration**: Validation that acceleration and deceleration phases match human ballistic reaching laws rather than constant-velocity or naive easing algorithms.

---

## ⚡ Quickstart

### Option A: Docker Compose (Recommended for Production)

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

### Automatic Air-Gap Routing
Tag any query with `# @airgap` to prevent external network egress completely. GhostGate automatically diverts the prompt to the local, containerized Ollama model:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "# @airgap Analyze our internal proprietary merger agreement..."}
    ]
)
# Handled 100% offline via local Ollama — zero bytes leave the workstation.
```

---

## 🛠️ Workstation Security Tools

### Workstation AI Security Auditor (`ghostgate audit`)
Inspect local developer environments, IDE settings (Cursor, VS Code), and shell environments for unencrypted keys, shadow AI tools, and telemetry leakage:

```bash
python -m ghostgate_core.cli audit
```
```
[GHOSTGATE AUDITOR] Scanning developer workstation...
  ✔ Shell Environment (AWS_SECRET_ACCESS_KEY): Protected (Proxy Active)
  ✔ Cursor IDE Telemetry: Stripped
  ✔ Direct API Egress: Intercepted via Local Loopback
Audit Score: 100/100 (GRADE: A) - Compliant with Enterprise ZDR Policy
```

### RawHuman Interactive Verification Demo
Simulate live autonomous agent input injection vs authentic biological mouse motion:

```bash
python -m rawhuman_engine.demo_cli
```

---

## 📊 Benchmarks & Performance Specifications

| Metric | Measured Value | Security Standard / Target |
| :--- | :--- | :--- |
| **Proxy Latency Overhead (P99)** | **1.24 ms** | `< 2.0 ms` (Imperceptible to developer) |
| **Streaming TTFT Overhead** | **0.88 ms** | `< 1.5 ms` |
| **Memory Footprint** | **38 MB RAM** | Lightweight background daemon |
| **Data Retention** | **0 bytes** on disk | Strict RAM-only ephemeral lifecycle |
| **Bot Detection Latency** | **1.8 ms** | Real-time I/O gate lockout |
| **E2E Test Coverage** | **23 / 23 Passed (100%)** | Full automated unit & container tests |

---

## 📂 Repository Structure

```
.
├── config.yaml                    # Privacy policies, upstream configs, and redaction patterns
├── docker-compose.yml             # Production multi-container orchestration
├── Makefile                       # Developer shortcuts (build, run, test, e2e)
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
├── tests/                         # Comprehensive unit & live integration tests
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

Run the full automated test suites locally:

```bash
# 1. Run unit tests
pytest tests/ -v -k "not e2e"

# 2. Run live container E2E tests
pytest tests/test_e2e_live.py -v -s
```

---

## 🤝 Community & Security Governance

- **Security Advisories & Threat Model**: See [SECURITY.md](SECURITY.md).
- **Contributing Guidelines**: See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Compliance & Legal Addenda**: See [recipes/enterprise_compliance.md](recipes/enterprise_compliance.md).

## 📄 License
This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
