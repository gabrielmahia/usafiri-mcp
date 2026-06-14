# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for usafiri-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/usafiri-mcp"
LABEL org.opencontainers.image.description="usafiri-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir usafiri-mcp

CMD ["usafiri-mcp"]
