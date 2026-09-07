<p align="center">
  <h1 align="center">🛡️ GHOSTGATE & RAWHUMAN</h1>
  <p align="center">
    <strong>The Agentic Air-Gap OS: Human-in-the-Loop Security for the Autonomous AI Era</strong><br>
    <em>Outbound Format-Preserving Data Sovereignty & Inbound Kernel/I/O Proof-of-Human Sentinel</em>
  </p>
  <p align="center">
    <a href="https://github.com"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
    <a href="https://github.com"><img src="https://img.shields.io/badge/python-3.9%2B-brightgreen.svg" alt="Python Version"></a>
    <a href="https://github.com"><img src="https://img.shields.io/badge/Format--Preserving-Synthetic_Shadowing-emerald.svg" alt="Format Preserving"></a>
    <a href="https://github.com"><img src="https://img.shields.io/badge/HITL_Gateway-Active-indigo.svg" alt="HITL Gateway"></a>
    <a href="https://github.com"><img src="https://img.shields.io/badge/SOC_Dashboard-Port_8080-cyan.svg" alt="SOC Dashboard"></a>
  </p>
</p>

---

## ⚡ The Double-Sided AI Crisis

As AI shifts from conversational chatbots to autonomous agents commanding operating systems, legacy security perimeters have completely collapsed:

1. **Outbound IP & Secret Leakage**: Standard commercial LLM APIs retain prompts in plaintext for **30 to 90 days** for "abuse monitoring." When developers paste code, DB strings, or keys into prompts, secrets are exfiltrated to remote cloud logs. Competitor tools break LLM reasoning by inserting bracketed tags (`[REDACTED_...]`).
2. **Inbound Agent Takeovers & CAPTCHA Death**: Multimodal AI Agents (Anthropic Computer Use, OpenAI Operator) view desktop pixels and inject native OS mouse/keyboard commands. Browser-level CAPTCHAs (`event.isTrusted`) are obsolete.

**GhostGate Labs** unifies both perimeters into a single, cohesive **Agentic Air-Gap OS**:

```mermaid
graph TD
    subgraph OUTBOUND ["1. Outbound Protection: GhostGate Proxy (:8080)"]
        Dev[Engineer / IDE / CI Pipeline] -->|Prompt with Secrets| Proxy[GhostGate Proxy :8080]
        Proxy -->|Format-Preserving Engine| Redactor[Synthetic Shadowing]
        Redactor -->|Valid Mock Keys: AKIA... exact 20 chars| CloudLLM[Commercial Cloud LLM]
        Redactor -->|Air-Gap Trigger #@airgap| LocalLLM[100% Offline Local Ollama]
        CloudLLM -->|Streamed SSE Response| Proxy
        Proxy -->|In-Memory Rehydration| Dev
    end

    subgraph INBOUND ["2. Inbound & HITL Protection: RawHuman Sentinel (:8081)"]
        CloudLLM -->|Autonomous Tool Call: bash, db_delete| Gateway[HITL Execution Gateway]
        Gateway -->|Halt & Query Physical Presence| RawHuman[RawHuman I/O Sentinel]
        RawHuman -->|Check Kernel Injection Flags LLMHF_INJECTED| KernelCheck{OS Flags & Jitter}
        RawHuman -->|8-12Hz Tremor + Fitts's Ballistics| BioCheck{Biomechanics}
        RawHuman -->|Multi-Modal Fallback| TouchID[Hardware TouchID / WebAuthn]
        KernelCheck -->|Pass| Exec[Execute Tool Call]
        BioCheck -->|Pass| Exec
        TouchID -->|Pass| Exec
        KernelCheck -->|Synthetic Injected: 0.002s latency| Block[Block Agent Takeover]
        BioCheck -->|Zero Tremor: 0.002s latency| Block
    end
```

---

## 🚀 60-Second Quickstart

### 1. Installation
```bash
git clone https://github.com/ghostgate/ghostgate.git
cd ghostgate
make install
```

### 2. Launch GhostGate AI Privacy Proxy & CISO Dashboard
```bash
make run-proxy
```
* **AI Proxy Endpoint:** `http://127.0.0.1:8080/v1`
* **Real-time CISO SOC Dashboard:** Open browser at `http://127.0.0.1:8080/dashboard`

Point any OpenAI or Anthropic SDK:
```python
from openai import OpenAI

# Automatically performs format-preserving redaction and in-memory rehydration
client = OpenAI(base_url="http://127.0.0.1:8080/v1")
```

### 3. Run RawHuman Proof-of-Human Interactive Demo
```bash
make demo
```
Watch the biomechanical engine evaluate **8–12Hz neuromuscular tremor**, **Fitts's Law ballistic curves**, and **OS synthetic event flags (`LLMHF_INJECTED`)** to terminate autonomous agent takeovers in 2ms.

---

## 🔑 Key Features

### 🛡️ GhostGate Core (Outbound Data Sovereignty)
* **Format-Preserving Synthetic Shadowing**: Replaces secrets with syntactically valid mock values of identical length and character set (`AKIAIOSFODNN7EXAMPLE` ➔ `AKIA7B8C9D0E1F2G3H4I`). Prevents LLM code generation syntax breakage and regex hallucinations!
* **Zero Data Retention Enforcer**: Strips client tracking cookies, telemetry fingerprints (`x-stainless-*`), and forces strict ZDR headers.
* **Dynamic Air-Gap Interception**: Queries flagged with `# @airgap` or unencrypted private keys are routed away from cloud servers to local containerized models (Ollama/vLLM).
* **Zero-Training Recipe Matrix**: Audit-ready compliance recipes for OpenAI, Anthropic, Google Gemini, Cursor, Copilot, and Perplexity.

### 🧬 RawHuman & HITL Gateway (Inbound Agent Defense)
* **Human-in-the-Loop (HITL) Execution Gateway**: Intercepts dangerous autonomous agent tool calls (`execute_bash`, `delete_database`, `deploy_production`) and requires physical human presence verification.
* **Kernel & I/O Origin Detection**: Inspects low-level OS event pipelines (`LLMHF_INJECTED`, `CGEventSourceStateID`) to detect programmatic event synthesis.
* **Biomechanical Physics Engine**: Evaluates muscle inertia, ballistic velocity profiles, and physiological tremors (8–12Hz biological oscillations) that pure mathematical Bezier curves lack.
* **Adaptive Sensor & TouchID Fallback**: Trackpad touch smoothing compensation and hardware TouchID/WebAuthn fallback guarantee zero false-positive lockouts under ADA accessibility regulations.

### 📊 Real-Time CISO & SOC Web Dashboard
* Built directly into the proxy at `http://127.0.0.1:8080/dashboard`.
* Live KPI cards (Prompts Inspected, Secrets Masked, Hijacks Blocked, ZDR Compliance 99.8%).
* Chart.js visualizations for masked secret distribution and I/O attestation telemetry.
* Live forensic event tail with one-click export for SOC2 and HIPAA compliance audits.

---

## 📁 Repository Structure

```
.
├── config.yaml                    # Privacy policies, upstream configs, and redaction patterns
├── Makefile                       # One-command orchestration
├── pyproject.toml                 # Package configuration
├── requirements.txt               # Dependencies
├── ghostgate_core/                # Outbound reverse proxy and secret rehydration
│   ├── proxy.py                   # Async FastAPI reverse proxy
│   ├── redactor.py                # Format-preserving synthetic shadowing engine
│   ├── zdr_enforcer.py            # Telemetry stripper and ZDR policy checker
│   ├── hitl_gateway.py            # Human-in-the-Loop tool call execution gateway
│   ├── dashboard.py               # Embedded CISO Security Operations Center web UI
│   └── airgap/                    # Docker Compose air-gap stack for Ollama & WebUI
├── rawhuman_engine/               # Inbound kernel & I/O Proof-of-Human engine
│   ├── detector.py                # OS synthetic injection flag hooks
│   ├── biomechanics.py            # Fitts's law, 8-12Hz micro-tremor & TouchID fallback
│   ├── server.py                  # Attestation daemon API
│   └── demo_cli.py                # Terminal visualizer for bot vs human telemetry
├── recipes/                       # The Zero-Training Recipe Matrix
│   ├── RECIPE_MATRIX.md           # Audit matrix for OpenAI, Anthropic, Google, Cursor, etc.
│   ├── enterprise_compliance.md   # Legal DPA Zero-Retention addendum and internal AUP
│   └── developer_cheatsheet.md    # 60-second setup for engineers
├── tests/                         # 16 Unit & integration test suite (100% pass)
└── vc_pitch_package/              # Institutional fundraising materials
    ├── PITCH_DECK.md              # 15-slide VC pitch deck (Agentic Air-Gap OS)
    ├── EXECUTIVE_SUMMARY.md       # 1-pager investment memo
    ├── VC_OBJECTIONS_FAQ.md       # Technical defense against top investor objections
    ├── ENTERPRISE_PILOT_AGREEMENT.md # 90-day Paid Enterprise Proof-of-Concept contract
    ├── FINANCIAL_MODEL.md         # 5-year ARR, hybrid pricing & pilot economics
    └── VIRAL_LAUNCH_PLAYBOOK.md   # LinkedIn, Hacker News, and X distribution playbooks
```

---

## 🧪 Testing & Verification

Run the comprehensive unit and integration test suite:
```bash
make test
```

---

## 📄 License & Community
Apache 2.0. Built for developers and security teams demanding true AI sovereignty.
