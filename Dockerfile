FROM python:3.13-bookworm

# Variables de entorno
ENV FASTAPI_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/buscador/.local/bin

# Crear usuario del sistema sin privilegios
RUN useradd --create-home --home-dir /home/buscador buscador  


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/buscador

USER  buscador

COPY --chown=buscador:buscador pyproject.toml ./

RUN pip install --no-cache-dir --user .

COPY --chown=buscador:buscador ./app ./app
COPY --chown=buscador:buscador ./alembic ./alembic
COPY --chown=buscador:buscador main.py alembic.ini .env-example ./


EXPOSE 8000

# Comando para correr la FastAPI apuntando a main:app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]