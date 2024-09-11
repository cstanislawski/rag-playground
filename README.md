# RAG Playground

Playground for RAG (Retrieval-Augmented Generation) locally / on-prem

This project implements a RAG system using Postgres with pgvector for efficient similarity search, and Ollama for embeddings and text generation.

## Features

- Easy setup and cleanup scripts
- Vector similarity search using pgvector
- Local embedding generation with Ollama
- Text generation using Ollama models
- Multiple interaction modes:
  - Single query mode
  - Continuous mode for multiple one-turn queries
  - Multi-turn conversation mode with context retention

## Prerequisites

- Docker
- Python3
- Ollama CLI installed (for local embedding generation and text generation)

## Data

- [seed_data.json](data/seed_data.json) - Seed data for the playground with embeddings for products, copied over from [Azure-Samples/rag-postgres-openai-python](https://github.com/Azure-Samples/rag-postgres-openai-python)
- [seed_data_no_embeds.json](data/seed_data_no_embeds.json) - Same seed data but without embeddings, for testing generating embeddings

## Setup

- Clone this repository:

```bash
git clone https://github.com/your-username/rag-playground
cd rag-playground
```

- Run the preparation script:

```bash
chmod +x prepare.sh
./prepare.sh
```

This script will:

- Pull the required Ollama models
- Set up a Python virtual environment
- Install the required Python packages
- Create a `.env` file from `.env.example`
- Start the Postgres database with pgvector

- Update the `.env` file with your specific configuration if needed.

- Load the sample data and create embeddings:

```bash
python3 main.py setup
```

## Usage

Ensure your Python virtual environment is activated:

```bash
source venv/bin/activate
```

### Single Query Mode

Run a single search query:

```bash
python3 main.py search --query "Your search query here"
```

Example:

```bash
python3 main.py search --query "I need a waterproof jacket for hiking below $1- USD"
```

### Continuous Mode

Run multiple one-turn queries in succession:

```bash
python3 main.py search --continuous
```

In continuous mode, you can use the following commands:

- `help`: Display available commands
- `clear`: Clear the screen
- `exit`: Exit the program

### Multi-turn Conversation Mode

Engage in a multi-turn conversation with context retention:

```bash
python3 main.py search --multi-turn
```

In multi-turn mode, you can use the following commands:

- `help`: Display available commands
- `clear`: Clear the screen
- `clear history`: Clear the conversation history
- `exit`: Exit the program

## Customization

- To add more products or update existing ones, modify the `data/seed_data_no_embeds.json` file and re-run the setup process.
- Adjust the number of results returned by modifying the `n` parameter in the `vector_similarity_search` function in `rag_search.py`.
- Change the language model for response generation by updating the `TEXT_GEN_MODEL_NAME` in your `.env` file.

## Cleanup

To remove all generated files, stop containers, and clean up the project:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

## Troubleshooting

If you encounter any issues:

1. Ensure that Docker is running and that you have the necessary permissions.
2. Check that Ollama is installed correctly and the required models are available.
3. Verify that your `.env` file is configured correctly.
4. If you're having database connection issues, ensure that the Postgres container is running and that the connection details in your `.env` file are correct.

If problems persist, please open an issue in the GitHub repository with a detailed description of the error and the steps to reproduce it.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
