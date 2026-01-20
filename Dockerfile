FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Installer DuckDB CLI
RUN wget https://github.com/duckdb/duckdb/releases/download/v1.4.3/duckdb_cli-linux-amd64.zip \
    && unzip duckdb_cli-linux-amd64.zip \
    && mv duckdb /usr/local/bin/ \
    && rm duckdb_cli-linux-amd64.zip

# Installer packages Python
RUN pip install --no-cache-dir \
    duckdb==1.4.3 \
    pandas==2.3.3 \
    openpyxl==3.1.5 \
    pyyaml==6.0.3 \
    scipy==1.17.0

WORKDIR /app