# The Zero-Training & Zero Data Retention (ZDR) Master Recipe Matrix

This document provides a battle-tested, authoritative breakdown of data retention, training policies, and opt-out paths across all major commercial LLM providers, developer tools, and consumer interfaces.

---

## 1. Executive Summary: The "Data Training" Landscape

| Provider & Tier | Web/Consumer UI Trains? | API Trains by Default? | Plaintext Retention Window | How to Enforce Zero Data Retention (ZDR) |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI (ChatGPT Free/Plus)** | **YES (Default ON)** | N/A | Infinite / Account deletion | Data Controls -> Disable "Improve model for everyone" |
| **OpenAI (Team / Enterprise)** | NO | N/A | Workspace retention rules | Contractual enterprise agreement |
| **OpenAI API** | NO | **NO** | **30 Days (Abuse logs)** | Apply for bespoke ZDR eligibility via Sales OR use GhostGate |
| **Anthropic (Claude Free/Pro)** | NO (Unless thumbs-up) | N/A | Up to 2 years (or 30 days) | Privacy Settings -> Opt out |
| **Anthropic API** | NO | **NO** | **30 Days (Abuse logs)** | Formal ZDR SLA required for 0-day retention OR use GhostGate |
| **Google Gemini (Consumer)** | **YES (Default ON)** | N/A | 18 Months (human-reviewed) | Gemini Apps Activity -> Turn OFF |
| **Google Cloud Vertex AI** | NO | **NO** | 0 Days (Customer VPC) | Compliant by default if Customer-Managed Encryption Key (CMEK) |
| **Cursor IDE** | **YES (Basic Mode)** | N/A | Varies | Enable "Privacy Mode" in Settings (Mandatory) |
| **GitHub Copilot** | **YES (Individual)** | N/A | 28 Days | Disable "Allow GitHub to use my code snippets for model training" |
| **Perplexity AI** | **YES (Default ON)** | NO | Search history saved | Account Settings -> AI Data Retention -> OFF |

---

## 2. Provider-by-Provider Step-by-Step Recipes

### 2.1 OpenAI
* **API Policy**: By default, data submitted to the OpenAI API is **not** used to train OpenAI models. However, requests are stored in plaintext for up to **30 days** on OpenAI servers for abuse and misuse monitoring.
* **How to eliminate 30-Day Retention**:
  1. OpenAI requires organizations to apply for a formal **Zero Data Retention (ZDR)** agreement with their sales team.
  2. Eligibility typically requires minimum annual commitments and enterprise compliance justification (HIPAA, SOC2, PCI-DSS).
* **GhostGate Solution**: If you do not have an enterprise ZDR contract, GhostGate automatically masks all secrets, credentials, and PII before dispatch, rendering any 30-day logs harmless.
* **ChatGPT Web Opt-Out**:
  1. Click Profile Avatar -> **Settings** -> **Data Controls**.
  2. Toggle **Improve the model for everyone** to **OFF**.
  3. Direct Opt-Out Privacy Form: `https://privacy.openai.com`

---

### 2.2 Anthropic Claude
* **API Policy**: Anthropic does not train commercial models on your API inputs or outputs. Data is retained for **30 days** to support safety and misuse detection (with exceptions for certain specialized models).
* **How to verify ZDR status**:
  1. Navigate to Claude Console -> **Settings** -> **Privacy Controls**.
  2. Inspect the **Data retention period** field.
  3. If your enterprise has a ZDR agreement, this field will show `0 days`.
* **Claude.ai Web Interface**:
  1. Navigate to **Account** -> **Privacy**.
  2. Verify that chat history training options are disabled.

---

### 2.3 Google Gemini & Vertex AI
* **Consumer Gemini (`gemini.google.com`)**:
  - **High Danger**: By default, human reviewers read and annotate conversations. These snippets are disconnected from your Google Account but retained for up to 3 years.
  - **Hardening Recipe**: Go to `https://myactivity.google.com/product/gemini` -> Set **Gemini Apps Activity** to **Turn off and delete activity**.
* **Enterprise Google Cloud Vertex AI**:
  - Enterprise-grade isolation: Vertex AI does not log or train on customer prompts.
  - Recommended config: Deploy Gemini 1.5/2.0 inside a Google Cloud VPC with Private Service Connect (PSC).

---

### 2.4 Developer IDEs (Cursor, Copilot, Windsurf)

#### Cursor IDE (Crucial for Engineers)
* In standard mode, Cursor can transmit prompt context and code indices to third-party endpoints.
* **Mandatory Hardening Recipe**:
  1. Open Cursor Settings (`Cmd + ,` or `Ctrl + ,`).
  2. Search for **Privacy Mode**.
  3. Set **Privacy Mode** to **ON**.
  4. In `cursor.json`: `"cursor.privacyMode": true`.
  5. Point Cursor API base URL to `http://localhost:8080/v1` (GhostGate Proxy) to ensure real-time credential masking.

#### GitHub Copilot
* For individual accounts:
  1. Navigate to GitHub -> **Settings** -> **Copilot**.
  2. Uncheck **Allow GitHub to use my code snippets from the code editor for product improvements**.
* For GitHub Enterprise:
  1. Organization Owners must set Copilot Policy to **Blocked** for public code suggestions and telemetry harvesting.

---

## 3. GhostGate Automated Defense Matrix

| Threat Category | Without GhostGate | With GhostGate Proxy (`localhost:8080`) |
| :--- | :--- | :--- |
| **AWS / GCP / DB Credentials** | Sent in plaintext to LLM servers; retained for 30 days in logs | Replaced with format-preserving synthetic shadow (e.g. `AKIA7B8C9D0E1F2G3H4I`); never leaves RAM |
| **Customer PII (Emails, Phones)** | Subject to subpoena or external breach during retention | Replaced with deterministic surrogate tokens; rehydrated on return |
| **Source Code Fingerprinting** | SDK user-agent & telemetry headers transmitted to vendor | All tracking & telemetry headers stripped; clean ZDR headers injected |
| **Accidental Secret Paste** | Immediately logged to remote vendor servers | High-entropy scanner catches string and halts/masks transmission |
| **Classified Code (`# @airgap`)** | Exfiltrated to cloud APIs | Dynamically intercepted and routed to offline local LLM (Ollama/vLLM) |
