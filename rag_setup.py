import json
import psycopg2
from psycopg2.extras import execute_values
import ollama
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


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


def load_data():
    try:
        with open("data/seed_data_no_embeds.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("seed_data_no_embeds.json file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from seed_data_no_embeds.json")
        raise


def generate_embeddings(data):
    embeddings_model = os.getenv("EMBEDDINGS_MODEL_NAME")
    for item in data:
        try:
            embedding = ollama.embeddings(
                model=embeddings_model, prompt=item["description"]
            )
            item["embedding"] = embedding["embedding"]
        except Exception as e:
            logger.error(f"Error generating embedding for item {item['id']}: {e}")
            item["embedding"] = None
    return data


def create_table(cur):
    try:
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
    except psycopg2.Error as e:
        logger.error(f"Error creating table: {e}")
        raise


def insert_data(cur, data):
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
        if item["embedding"] is not None
    ]
    try:
        execute_values(cur, insert_query, values)
    except psycopg2.Error as e:
        logger.error(f"Error inserting data: {e}")
        raise


def main():
    logger.info("Starting data loading process")
    data = load_data()
    data_with_embeddings = generate_embeddings(data)

    conn = connect_to_db()
    cur = conn.cursor()

    try:
        create_table(cur)
        insert_data(cur, data_with_embeddings)
        conn.commit()
        logger.info("Data loaded successfully!")
    except Exception as e:
        conn.rollback()
        logger.error(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
