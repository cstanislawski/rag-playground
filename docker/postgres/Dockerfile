FROM postgres:16.4

RUN apt-get update \
    && apt-get install -y postgresql-16-pgvector \
    && rm -rf /var/lib/apt/lists/*
