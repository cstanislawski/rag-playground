#!/bin/bash

if ! docker info &> /dev/null; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

if ! ollama --version &> /dev/null; then
    echo "ollama is not installed. Please install ollama and try again."
    exit 1
fi

echo "Pulling nomic-embed-text from ollama for generating embeddings"
ollama pull nomic-embed-text

echo "Starting a Python virtual environment and installing requirements"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating .env file from .env.example"
cp .env.example .env
echo "Please update the .env file with your specific configuration if needed."

echo "Setup complete. To activate the virtual environment, run:"
echo "source venv/bin/activate"
