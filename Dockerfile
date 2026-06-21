# Etapa de construcción
FROM python:3.13-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar uv en una sola capa y limpiar
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && apt-get purge -y --auto-remove ca-certificates curl \
    && rm -rf /var/lib/apt/lists/* /root/.local/bin

# Copiar dependencias primero
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copiar código
COPY ./app ./app
COPY ./alembic ./alembic
COPY main.py alembic.ini ./

# Etapa de runtime
FROM python:3.13-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1
ENV FASTAPI_ENV=production
ENV VIRTUAL_ENV=/opt/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH

# Crear usuario no root
RUN useradd --create-home --home-dir /home/buscador buscador

WORKDIR /home/buscador/app

# Copiar entorno virtual desde builder
COPY --from=builder /app/.venv $VIRTUAL_ENV
RUN chown -R buscador:buscador $VIRTUAL_ENV

# Copiar código con permisos correctos
COPY --from=builder --chown=buscador:buscador /app/app ./app
COPY --from=builder --chown=buscador:buscador /app/alembic ./alembic
COPY --from=builder --chown=buscador:buscador /app/main.py /app/alembic.ini ./

USER buscador

EXPOSE 8000

CMD ["/opt/venv/bin/python", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app", "--workers", "4", "--log-level", "info"]


