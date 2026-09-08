# Contributing to GhostGate

Thank you for your interest in contributing to GhostGate! GhostGate is an open-source security gateway safeguarding developer privacy and defending systems against autonomous AI agent takeovers.

---

## 🧭 Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for all contributors. Please treat all members of the community with respect and professional courtesy.

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.10+ (Python 3.11, 3.12, 3.13, 3.14 supported)
- Docker & Docker Compose (for local containerized testing)
- `git` and standard build tools

### Local Environment Setup
```bash
# 1. Clone the repository
git clone https://github.com/MinsuKin/ghostgate.git
cd ghostgate

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install development dependencies
pip install --upgrade pip
pip install -e ".[dev]"
# Or: pip install -r requirements.txt
```

---

## 🧪 Running Tests

GhostGate maintains a strict testing policy. All pull requests must pass the complete test suite.

### Running Unit Tests
```bash
# Run unit tests
pytest tests/ -v -k "not e2e"
```

### Running Live E2E Container Tests
The live E2E test suite validates the full proxy stack against containerized services:
```bash
# 1. Start the stack in Docker
docker compose up -d --build

# 2. Run live end-to-end integration tests
pytest tests/test_e2e_live.py -v -s

# 3. Teardown
docker compose down
```

---

## 📐 Architecture & Contribution Guidelines

When submitting code changes, please observe the following architectural rules:

1. **Zero Data Retention (ZDR) Principle:**
   - Never write sensitive prompts, raw credentials, or unmasked tokens to persistent disk, stdout logs, or telemetry collectors.
   - All format-preserving shadowing lookup tables must remain strictly in memory and ephemeral.

2. **Technical Rigor & Mathematical Grounding:**
   - In `rawhuman_engine/`, all I/O analysis must be grounded in verified operating system event APIs (e.g. Win32 `winuser.h`, macOS Quartz Event Services, Linux `evdev`) and validated kinematic models (directional curvature entropy, Fitts's Law ballistic curves, discrete timer jitter).
   - Avoid biological or unverifiable marketing buzzwords.

3. **Format Preservation Integrity:**
   - Any additions to `ghostgate_core/redactor.py` regex detectors must generate shadow tokens that preserve length, entropy, and character grammar so downstream LLM AST parsers do not fail.

4. **Commit Conventions:**
   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New features
   - `fix:` Bug fixes
   - `refactor:` Code restructuring without behavior changes
   - `docs:` Documentation improvements
   - `test:` Adding or updating tests
   - `perf:` Performance optimizations

---

## 🚀 Submitting a Pull Request

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Write unit tests covering your changes.
3. Verify all tests pass locally:
   ```bash
   pytest tests/ -v
   ```
4. Push to your fork and submit a Pull Request targeting `main`.
5. Clearly describe the problem your PR solves, your technical approach, and test verification output in the PR description.
