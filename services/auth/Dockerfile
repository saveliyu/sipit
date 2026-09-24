FROM python:3.14-slim AS builder

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir "poetry>=2.2"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ARG INTEGRATIONAL_ARGS="--without dev"

RUN poetry install ${INTEGRATIONAL_ARGS} --no-root

FROM python:3.14-slim AS runner
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]