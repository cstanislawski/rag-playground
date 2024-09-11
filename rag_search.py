import psycopg2
import numpy as np
import ollama
from typing import List, Tuple


def connect_to_db():
    return psycopg2.connect(
        host="localhost", database="postgres", user="postgres", password="postgres"
    )


def vector_similarity_search(
    query: str, max_price: float = float("inf"), n: int = 5
) -> List[Tuple[int, str, str, float, float]]:
    # Generate embedding for the query
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query)[
        "embedding"
    ]

    conn = connect_to_db()
    cur = conn.cursor()

    # Perform similarity search with price filter
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

    cur.close()
    conn.close()

    return results


def generate_response(
    query: str, results: List[Tuple[int, str, str, float, float]]
) -> str:
    # Prepare context from search results
    context = "\n".join(
        [
            f"Product: {name}\nDescription: {desc[:200]}...\nPrice: ${price:.2f}"
            for _, name, desc, price, _ in results
        ]
    )

    # Prepare prompt for gemma2:2b
    prompt = f"""Given the following product descriptions:

{context}

Please answer the following query from a customer:
"{query}"

Provide a helpful response based on the given product information. Be concise and informative. Refer to products by their names and include their prices."""

    # Generate response using gemma2:2b
    response = ollama.generate(model="gemma2:2b", prompt=prompt)

    return response["response"]


def rag_pipeline(query: str) -> str:
    # Extract price limit from query if present
    max_price = float("inf")
    if "below" in query.lower() and "usd" in query.lower():
        try:
            price_str = query.lower().split("below")[1].split("usd")[0].strip()
            max_price = float(price_str.replace("$", "").strip())
        except ValueError:
            pass  # If we can't parse the price, we'll use the default max_price

    # Retrieve similar products
    results = vector_similarity_search(query, max_price)

    # Generate a response based on the retrieved information
    response = generate_response(query, results)

    return response


# Test the RAG pipeline
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
