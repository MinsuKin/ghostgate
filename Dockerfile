# GhostGate & RawHuman Production Dockerfile
# Multi-arch, hardened, unprivileged container

FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set up non-root user
RUN groupadd -g 10001 ghostgate && \
    useradd -u 10001 -g ghostgate -m -s /bin/bash ghostgate

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY --chown=ghostgate:ghostgate config.yaml pyproject.toml ./
COPY --chown=ghostgate:ghostgate ghostgate_core/ ./ghostgate_core/
COPY --chown=ghostgate:ghostgate rawhuman_engine/ ./rawhuman_engine/
COPY --chown=ghostgate:ghostgate recipes/ ./recipes/
COPY --chown=ghostgate:ghostgate tests/ ./tests/

# Switch to unprivileged user
USER ghostgate

# Expose ports: 8080 (GhostGate Proxy & Dashboard), 8081 (RawHuman Sentinel)
EXPOSE 8080 8081

ENV PYTHONUNBUFFERED=1 \
    GHOSTGATE_HOST=0.0.0.0 \
    GHOSTGATE_PORT=8080 \
    RAWHUMAN_HOST=0.0.0.0 \
    RAWHUMAN_PORT=8081

# Health check against GhostGate proxy endpoint
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default entrypoint runs GhostGate Proxy
CMD ["python", "-m", "ghostgate_core.proxy"]
