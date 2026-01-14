FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /home
COPY ./server .

COPY pyproject.toml .
RUN uv sync --project pyproject.toml

CMD [".venv/bin/fastapi", "run", "main.py", "--port", "8001"]