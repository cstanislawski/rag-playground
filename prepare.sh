#! /bin/bash

echo "Pulling nomic-embed-text from ollama for generating embeddings"
ollama pull nomic-embed-text

echo "Starting a Python virtual environment and installing requirements"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
