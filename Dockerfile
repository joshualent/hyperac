FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

RUN uv sync --frozen --no-dev

ENV DEBUG=False \
    DJANGO_VITE_DEV_MODE=false

RUN uv run python manage.py collectstatic --noinput


FROM python:3.13-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    DEBUG=False \
    DJANGO_VITE_DEV_MODE=false \
    HOME=/app \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --system app && useradd --system --gid app app

COPY --from=builder --chown=app:app /app /app

USER app

EXPOSE 8000

CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000", "--no-control-socket"]

