# Security Policy

GhostGate is an open-source security gateway designed to protect developer secrets, proprietary intellectual property, and local endpoints from unauthorized AI data exfiltration and autonomous agent takeovers. We take security vulnerabilities seriously and appreciate responsible disclosure.

---

## 🔒 Reporting a Vulnerability

If you believe you have discovered a security vulnerability in GhostGate or the RawHuman Sentinel, please report it via **GitHub Private Vulnerability Reporting** under the Security tab of our repository, or email the maintainers directly:

- **Security Email:** `security@ghostgate.dev`
- **PGP Fingerprint (optional):** Available upon request.
- **Response Commitment:** 
  - Initial acknowledgement and triage within **48 hours**.
  - Status updates every **72 hours** until resolution.
  - Coordinated public disclosure with CVE assignment within **30 days** of patch verification.

Please do **not** file public GitHub issues or disclose vulnerabilities publicly until a fix has been released and verified.

---

## 🛡️ Threat Model & Security Boundaries

GhostGate operates as a **local loopback security intermediary** (`127.0.0.1`) and OS-level I/O sentinel. To set realistic security guarantees, our threat model is defined as follows:

### In-Scope Threats

1. **Third-Party Model Provider Exfiltration:**
   - Prompt retention, logging, and model fine-tuning on sensitive enterprise credentials (AWS tokens, GitHub PATs, private keys, database connection strings, customer PII).
   - Format-preserving synthetic shadowing replaces raw secrets in memory before egress, rehydrating them strictly upon stream return.
2. **Client-Side Telemetry Tracking:**
   - SDK telemetry headers (`x-stainless-*`, analytics cookies, user session fingerprints) leaking internal network topography to AI providers.
3. **Autonomous Agent Runaway & Tool Execution Hijacks:**
   - Multimodal desktop agents (e.g. Anthropic Computer Use, OpenAI Operator) issuing unauthorized programmatic API calls (`SendInput`, `CGEventPost`, `uinput`) to trigger destructive tool calls (`bash`, `db_drop`, `aws_terminate`).
   - Intercepted by the **RawHuman Sentinel** via OS hook flags and Kinematic Trajectory Dynamics.

### Out-of-Scope (Non-Threats)

1. **Compromised Ring 0 / Kernel-Level Rootkits:**
   - If an adversary has achieved kernel-mode code execution on the host machine, user-space proxies and hook detectors cannot provide cryptographic integrity guarantees.
2. **Physical Hardware Bus Taps & USB Microcontroller Implants:**
   - Custom malicious USB hardware devices (e.g. Teensy Rubber Ducky) presenting valid USB HID descriptor IDs at the electrical layer.
3. **Memory Scraping via Root / Administrator:**
   - Any process running as `root`/`SYSTEM` with `ptrace` or debugger attachments can inspect process RAM. GhostGate protects data in flight and enforces zero disk persistence.

---

## ⚙️ Low-Level OS Injection Detection Specifications

GhostGate's RawHuman Sentinel inspects native OS-level event generation flags to detect whether mouse or keyboard events originated from programmatic injection APIs rather than physical human hardware interrupts.

### 1. Windows (Win32 API)
Under Windows, simulated events generated via `SendInput` or `keybd_event`/`mouse_event` are tagged by the Windows subsystem in the low-level hook structures:
- **Low-Level Mouse Hook (`MSLLHOOKSTRUCT`):**
  - Bit 0 (`0x00000001`): `LLMHF_INJECTED` (Documented in Microsoft Win32 SDK `winuser.h`, introduced in Windows 2000). Specifies whether the event was injected from a process or originated from a physical mouse device.
  - Bit 1 (`0x00000002`): `LLMHF_LOWER_IL_INJECTED` (Windows 8+). Indicates injection from a lower Integrity Level process.
- **Low-Level Keyboard Hook (`KBDLLHOOKSTRUCT`):**
  - Bit 4 (`0x00000010`): `LLKHF_INJECTED`. Specifies synthetic keystroke injection.

### 2. macOS (Quartz Event Services)
On macOS, simulated events generated via `CGEventCreateMouseEvent`, `CGEventPost`, or AppleScript are tagged in Quartz event headers:
- `CGEventGetIntegerValueField(event, kCGEventSourceUserData)`
- Evaluation of `kCGEventSourceStatePrivate` vs `kCGEventSourceStateCombinedSessionState`
- Absence of IOHIDEvent driver-level timestamp monotonicity.

### 3. Linux (evdev & uinput)
On Linux systems:
- Differentiation between physical hardware input nodes (`/dev/input/by-id/usb-*`) and virtual synthetic device handles (`/dev/input/uinput` or XTEST extension events via `XRecord`/`XTestFakeMotionEvent`).

---

## 🔐 Cryptographic & Data Retention Guarantees

- **Zero Disk Persistence (ZDR):** GhostGate stores **zero** prompts, responses, or secret mappings on persistent storage. All synthetic shadowing dictionaries reside solely in RAM, scoped to the individual HTTP transaction, and are purged immediately after the stream closes.
- **Format-Preserving Entropy Engine:** Shadows are generated using high-entropy random generation matching the exact entropy, length, and character space of the target credential (e.g. AWS `AKIA[0-9A-Z]{16}`).
- **Local Air-Gap Isolation:** Sensitive prompts tagged with `# @airgap` or matching classification rules are routed to offline, containerized models (e.g., Ollama) with external network egress disabled.

---

## 🧪 Empirical Evaluation & Attack Corpus

To empirically test detection efficacy, GhostGate maintains a structured evaluation corpus in [`tests/corpus/`](tests/corpus/):
- `secrets_leakage_corpus.json`: Ground-truth test suite containing 22+ multi-cloud credentials, API keys, database connection strings, and negative controls.
- `synthetic_agent_corpus.json`: Trajectory datasets comparing programmatic automation tools (linear moves, cubic Bezier splines) against authentic human reaching movements.
- `adversarial_prompts_corpus.json`: Adversarial evasion prompts including direct instruction overrides and base64 obfuscation requests.

Run the evaluation suite locally:
```bash
pytest tests/test_attack_corpus.py -v
```

