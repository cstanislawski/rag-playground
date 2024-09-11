#!/bin/bash

echo "Cleaning up RAG project..."

# Stop and remove Docker containers
echo "Stopping and removing Docker containers..."
docker compose down -v

# Remove virtual environment
echo "Removing virtual environment..."
rm -rf venv

echo "Cleanup complete!"
