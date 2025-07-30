FROM python:3.11-slim

WORKDIR /app

# Install uv for package management
RUN pip install --no-cache-dir uv

# Install the mcp-server-aibtcdev package
RUN uv pip install --system --no-cache-dir mcp-server-aibtcdev

# Expose the default port for SSE transport
EXPOSE 8000

# Set environment variables with defaults that can be overridden at runtime
ENV AIBTC_API_BASE_URL="https://api.aibtc.dev"
ENV AIBTC_BEARER_TOKEN=""
ENV AIBTC_API_KEY=""
ENV AIBTC_WEBHOOK_AUTH_TOKEN=""

# Run the server with SSE transport
CMD uvx mcp-server-aibtcdev --transport sse