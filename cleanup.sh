#!/bin/bash

echo "Cleaning up RAG project..."

echo "Stopping and removing Docker containers..."
docker compose down -v

echo "Removing virtual environment..."
rm -rf venv

echo "Cleanup complete!"
