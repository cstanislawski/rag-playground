import json
import psycopg2
from psycopg2.extras import execute_values
import ollama
import numpy as np

# Load the data
with open("data/seed_data_no_embeds.json", "r") as f:
    data = json.load(f)

# Generate embeddings
for item in data:
    description = item["description"]
    embedding = ollama.embeddings(model="nomic-embed-text", prompt=description)
    item["embedding"] = embedding["embedding"]

# Connect to the database
conn = psycopg2.connect(
    host="localhost", database="postgres", user="postgres", password="postgres"
)

# Create a cursor
cur = conn.cursor()

# Create the table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        type VARCHAR(255),
        brand VARCHAR(255),
        name VARCHAR(255),
        description TEXT,
        price FLOAT,
        embedding vector(768)
    )
"""
)

# Insert the data
insert_query = """
    INSERT INTO products (type, brand, name, description, price, embedding)
    VALUES %s
"""

values = [
    (
        item["type"],
        item["brand"],
        item["name"],
        item["description"],
        item["price"],
        item["embedding"],
    )
    for item in data
]

execute_values(cur, insert_query, values)

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data loaded successfully!")
