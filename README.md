# RAG

Playground for RAG (Retrieval-Augmented Generation) locally / on-prem

This project implements a RAG system using Postgres with pgvector for efficient similarity search, and Ollama for embeddings and text generation.

## Data

- [seed_data.json](data/seed_data.json) - Seed data for the playground with embeddings for products, copied over from [Azure-Samples/rag-postgres-openai-python](https://github.com/Azure-Samples/rag-postgres-openai-python)
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
- Create a `.env` file from `.env.example`

- Update the `.env` file with your specific configuration if needed.

- Start the Postgres database with pgvector:

```bash
docker compose up -d
```

- Load the sample data and create embeddings:

```bash
python main.py setup
```

## Usage

To use the RAG search functionality:

- Ensure your Python virtual environment is activated:

```bash
source venv/bin/activate
```

- Run a search query:

```bash
python main.py search --query "Your search query here"
```

For example:

```bash
python main.py search --query "I need a waterproof jacket for hiking below $150 USD"
```

## Customization

- To add more products or update the existing ones, modify the `data/seed_data_no_embeds.json` file and re-run the setup process.
- You can adjust the number of results returned by modifying the `n` parameter in the `vector_similarity_search` function in `rag_search.py`.
- To use a different language model for response generation, update the `TEXT_GEN_MODEL_NAME` in your `.env` file.

## Cleanup

To remove all generated files, stop containers, and clean up the project:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

This script will:

- Stop and remove Docker containers
- Remove the virtual environment
- Delete the generated .env file
- Remove any log files (if present)

## Troubleshooting

- If you encounter issues with connecting to the database, ensure that the Postgres container is running (`docker compose ps`) and that the connection details in your `.env` file match those in the `docker compose.yml` file.
- If embeddings fail to generate, make sure the Ollama service is running and the specified embedding model is correctly installed.

## License

MIT - [LICENSE](./LICENSE)
