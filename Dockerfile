FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY design ./design
COPY tests ./tests

RUN pip install --upgrade pip && pip install -e .[dev]

ENV DDE_DATA_DIR=/app/.data/projects

CMD ["python", "-m", "domain_discovery_engine.interfaces.cli"]
