import argparse
from rag_setup import main as setup_main
from rag_search import rag_pipeline
import logging
import os
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("main")


def setup():
    logger.info("Running setup process")
    setup_main()


def search(query):
    logger.info(f"Executing search for query: {query}")
    response = rag_pipeline(query)
    print("\nResponse:")
    print(response)


def main():
    parser = argparse.ArgumentParser(description="RAG System CLI")
    parser.add_argument("action", choices=["setup", "search"], help="Action to perform")
    parser.add_argument("--query", help="Search query (required for 'search' action)")

    args = parser.parse_args()

    if args.action == "setup":
        setup()
    elif args.action == "search":
        if not args.query:
            parser.error("--query is required when action is 'search'")
        search(args.query)


if __name__ == "__main__":
    main()
