FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get update && \
    apt-get install -y git sudo npm curl && \
    rm -rf /var/lib/apt/lists/*

RUN npm i -g n && n lts && npm i -g npm@latest
RUN npm install -g @anthropic-ai/claude-code

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
ENTRYPOINT ["/entrypoint.sh"]
CMD ["claude"]

# Version labeling at the end to avoid cache invalidation
ARG CDOCK_VERSION=unknown
LABEL cdock.version="${CDOCK_VERSION}"
