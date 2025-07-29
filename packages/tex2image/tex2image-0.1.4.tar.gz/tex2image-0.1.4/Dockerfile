FROM kjarosh/latex:2025.1-basic

RUN tlmgr install standalone preview

RUN apk add poppler-utils python3

COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

WORKDIR /app

COPY src src
COPY README.md pyproject.toml uv.lock ./

ENV UV_COMPILE_BYTECODE=1
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --extra server
