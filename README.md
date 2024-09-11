# RAG

Playground for RAG (Retrieval-Augmented Generation) locally / on-prem

This project implements a RAG system using Postgres with pgvector for efficient similarity search, and Ollama for embeddings and text generation.

## Data

- [seed_data.json](data/seed_data.json) - Seed data for the playground with embeddings for --products, copied over from [Azure-Samples/rag-postgres-openai-python](https://github.com/Azure-Samples/rag-postgres-openai-python)
- [seed_data_no_embeds.json](data/seed_data_no_embeds.json) - Same seed data but without embeddings, for testing generating embeddings

## Prerequisites

- Docker
- Python3
- Ollama CLI installed (for local embedding generation)

## Setup

- Clone this repository:

```bash
git clone https://github.com/cstanislawski/rag
cd rag
```

- Run the preparation script:

```bash
chmod +x prepare.sh
./prepare.sh
```

This script will:

- Pull the `nomic-embed-text` model from Ollama
- Set up a Python virtual environment
- Install the required Python packages

- Start the Postgres database with pgvector:

```bash
docker-compose up -d
```

- Load the sample data and create embeddings:

```bash
python3 rag_setup.py
```

This script will load the product data from `data/seed_data_no_embeds.json`, generate embeddings using the Ollama model, and insert the data into the Postgres database.

## Usage

To use the RAG search functionality:

- Ensure your Python virtual environment is activated:

```bash
source venv/bin/activate
```

- Run the RAG search script:

```bash
python3 rag_search.py
```

This script includes some sample queries to demonstrate the functionality. You can modify the `test_queries` list in the script to try out different queries.

- To use the RAG system in your own Python code, you can import and use the `rag_pipeline` function from `rag_search.py`:

```python
from rag_search import rag_pipeline

query = "I need a waterproof jacket for hiking below $150 USD"
response = rag_pipeline(query)
print(response)
```

## Customization

- To add more products or update the existing ones, modify the `data/seed_data_no_embeds.json` file and re-run the `rag_setup.py` script.
- You can adjust the number of results returned by modifying the `n` parameter in the `vector_similarity_search` function in `rag_search.py`.
- To use a different language model for response generation, update the `ollama.generate()` call in the `generate_response` function in `rag_search.py`.

## Troubleshooting

- If you encounter issues with connecting to the database, ensure that the Postgres container is running (`docker-compose ps`) and that the connection details in the Python scripts match those in the `docker-compose.yml` file.
- If embeddings fail to generate, make sure the Ollama service is running and the `nomic-embed-text` model is correctly installed.

## License

MIT - [LICENSE](./LICENSE)
