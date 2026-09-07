# Developer 60-Second Hardening Cheatsheet

Protect your codebase, secrets, and API keys from leaking to AI models in under 60 seconds.

---

## 1. Terminal Environment Global Redirect
Redirect all CLI tools and Python/Node scripts that use the OpenAI SDK to route through GhostGate:

Add to your `~/.zshrc` or `~/.bashrc`:
```bash
# GhostGate Drop-in AI Proxy
export OPENAI_BASE_URL="http://127.0.0.1:8080/v1"
export ANTHROPIC_BASE_URL="http://127.0.0.1:8080/v1"
```
Apply changes:
```bash
source ~/.zshrc
```

---

## 2. Python SDK (Zero Code Modification)
When using the official `openai` Python package, GhostGate operates transparently:

```python
import os
from openai import OpenAI

# Automatically picks up OPENAI_BASE_URL from env, or specify directly:
client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Debug this AWS Key: AKIAIOSFODNN7EXAMPLE"}
    ]
)

# Secrets are redacted before leaving your machine,
# and automatically restored in response.choices[0].message.content!
print(response.choices[0].message.content)
```

---

## 3. Cursor IDE Setup
1. Press `Cmd + Shift + J` (or open Cursor Settings).
2. Go to **Features** -> **OpenAI / Model Configuration**.
3. Check **Override OpenAI Base URL**.
4. Set URL to: `http://127.0.0.1:8080/v1`.
5. Under **General**, verify **Privacy Mode** is set to `ON`.

---

## 4. Git Pre-Commit Privacy Hook
Prevent developers from committing prompts with unmasked credentials:

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Scan for high-entropy secrets in staged files
if git diff --cached | grep -E "(AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9]{20,})"; then
    echo "❌ [GhostGate Hook Error] High-entropy secret detected in staged commit!"
    echo "Please sanitize or run via GhostGate before committing."
    exit 1
fi
```
Make executable: `chmod +x .git/hooks/pre-commit`
