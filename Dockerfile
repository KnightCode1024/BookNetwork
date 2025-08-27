FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .

RUN chmod +x entrypoint.sh
