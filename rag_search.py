import psycopg2
import numpy as np
import ollama
from typing import List, Tuple
import os
from dotenv import load_dotenv
import logging
import httpx
from rich.logging import RichHandler

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rag")


class LoggingClient(httpx.Client):
    def send(self, request, **kwargs):
        logger.debug(f"HTTP Request: {request.method} {request.url}")
        response = super().send(request, **kwargs)
        logger.debug(f"HTTP Response: {response.status_code}")
        return response


ollama.client = LoggingClient()


def connect_to_db():
    try:
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    except psycopg2.Error as e:
        logger.error(f"Unable to connect to the database: {e}")
        raise


def vector_similarity_search(
    query: str, max_price: float = float("inf"), n: int = 5
) -> List[Tuple[int, str, str, float, float]]:
    try:
        query_embedding = ollama.embeddings(
            model=os.getenv("EMBEDDINGS_MODEL_NAME"), prompt=query
        )["embedding"]
    except Exception as e:
        logger.error(f"Error generating embedding for query: {e}")
        raise

    conn = connect_to_db()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT id, name, description, price, 1 - (embedding <=> %s::vector) AS similarity
            FROM products
            WHERE price <= %s
            ORDER BY similarity DESC
            LIMIT %s
            """,
            (query_embedding, max_price, n),
        )
        results = cur.fetchall()
    except psycopg2.Error as e:
        logger.error(f"Error executing similarity search query: {e}")
        raise
    finally:
        cur.close()
        conn.close()

    return results


def generate_response(
    query: str, results: List[Tuple[int, str, str, float, float]]
) -> str:
    context = "\n".join(
        [
            f"Product: {name}\nDescription: {desc[:200]}...\nPrice: ${price:.2f}"
            for _, name, desc, price, _ in results
        ]
    )

    prompt = f"""Given the following product descriptions:

{context}

Please answer the following query from a customer:
"{query}"

Provide a helpful response based on the given product information. Be concise and informative. Refer to products by their names and include their prices."""

    try:
        response = ollama.generate(
            model=os.getenv("TEXT_GEN_MODEL_NAME"), prompt=prompt
        )
        return response["response"]
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise


def rag_pipeline(query: str) -> str:
    logger.info(f"Processing query: {query}")
    max_price = float("inf")
    if "below" in query.lower() and "usd" in query.lower():
        try:
            price_str = query.lower().split("below")[1].split("usd")[0].strip()
            max_price = float(price_str.replace("$", "").strip())
            logger.info(f"Detected price limit: ${max_price:.2f}")
        except ValueError:
            logger.warning("Unable to parse price from query")

    try:
        results = vector_similarity_search(query, max_price)
        logger.info(f"Found {len(results)} relevant products")
        response = generate_response(query, results)
        return response
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {e}")
        return "I'm sorry, but I encountered an error while processing your request. Please try again later."


if __name__ == "__main__":
    test_queries = [
        "I need a waterproof jacket for hiking over $200 USD",
        "What's a good backpack for camping?",
        "Looking for comfortable hiking shoes",
    ]

    for query in test_queries:
        print(f"Query: {query}")
        print(rag_pipeline(query))
        print("-" * 50)
