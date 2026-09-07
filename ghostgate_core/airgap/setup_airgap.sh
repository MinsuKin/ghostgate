#!/usr/bin/env bash
# GhostGate Air-Gap Environment Provisioner
# Launches a 100% offline, local LLM stack with Zero Egress.

set -euo pipefail

echo "=========================================================="
echo "  🛡️  GhostGate Air-Gap Zero-Leak Local Stack Launcher"
echo "=========================================================="

if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed or not in PATH."
    echo "Please install Docker Desktop or run Ollama natively (https://ollama.ai)."
    exit 1
fi

echo "🚀 [1/3] Spinning up containerized Ollama & OpenWebUI..."
docker compose -f "$(dirname "$0")/docker-compose.yml" up -d

echo "⏳ [2/3] Waiting for Ollama runtime initialization..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
        echo "✅ Ollama daemon is ready!"
        break
    fi
    sleep 1
done

MODEL_NAME="${1:-qwen2.5-coder:7b}"
echo "📦 [3/3] Pulling privacy-hardened coding model: ${MODEL_NAME}..."
docker exec -it ghostgate-airgap-ollama ollama pull "${MODEL_NAME}"

echo "=========================================================="
echo "🎉 GhostGate Air-Gap Stack is LIVE and SECURE!"
echo " - Local API Endpoint : http://127.0.0.1:11434"
echo " - Web UI Interface   : http://127.0.0.1:3000"
echo " - Proxy Auto-Fallback: Ready on localhost:8080"
echo "=========================================================="
