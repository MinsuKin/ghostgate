.PHONY: help install run-proxy run-rawhuman demo test test-e2e bench docker-up docker-down prod-ready clean

help:
	@echo "GhostGate & RawHuman CLI Management:"
	@echo "  make install       - Install Python virtual environment & dependencies"
	@echo "  make run-proxy     - Launch GhostGate AI Privacy Proxy (Port 8080)"
	@echo "  make run-rawhuman  - Launch RawHuman I/O Attestation Server (Port 8081)"
	@echo "  make demo          - Run RawHuman interactive terminal demonstration"
	@echo "  make test          - Run unit, corpus, and integration test suite"
	@echo "  make test-e2e      - Execute full live End-to-End integration test suite"
	@echo "  make bench         - Execute statistical P50/P90/P99 latency & memory benchmark suite"
	@echo "  make docker-up     - Launch full containerized production stack in Docker"
	@echo "  make docker-down   - Stop and tear down containerized stack"
	@echo "  make prod-ready    - Validate complete production readiness & run all tests"
	@echo "  make clean         - Remove pycache and temporary files"

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run-proxy:
	. .venv/bin/activate && python -m ghostgate_core.proxy

run-rawhuman:
	. .venv/bin/activate && python -m rawhuman_engine.server

demo:
	. .venv/bin/activate && python -m rawhuman_engine.demo_cli

test:
	. .venv/bin/activate && pytest tests/ -v -k "not e2e"

test-e2e:
	. .venv/bin/activate && python -m pytest tests/test_e2e_live.py -v -s

bench:
	. .venv/bin/activate && python -m benchmarks.run_benchmarks

docker-up:
	docker compose up -d

docker-down:
	docker compose down

prod-ready: docker-up test test-e2e
	@echo "All production readiness checks and live E2E tests PASSED!"

airgap-up:
	bash ghostgate_core/airgap/setup_airgap.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
