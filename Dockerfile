FROM python:3.13-alpine

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
RUN pip install poetry==2.1.2 && poetry install --no-root

# Install node_modules lightGallery
COPY package.json package-lock.json ./
RUN apk add --no-cache nodejs npm && npm ci

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]