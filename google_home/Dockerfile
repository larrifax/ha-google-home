ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12-alpine3.19
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set environment
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install requirements
RUN apk add --no-cache \
    jq \
    && pip3 install --no-cache-dir \
    google-auth==2.28.0 \
    google-auth-oauthlib==1.2.0 \
    google-auth-httplib2==0.2.0 \
    aiohttp==3.13.3 \
    pydantic==2.6.1

# Copy application files
COPY rootfs /

# Make run script executable
RUN chmod a+x /run.sh

# Set working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD pgrep -f "python3 /app/main.py" || exit 1

# Start application
CMD ["/run.sh"]
