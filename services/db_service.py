"""
Brief: This file contains the functions to connect to the Astra database and upload data to a vector collection.

Description: This file contains the functions `connect_to_database`, `create_or_get_collection`, and 
`upload_csv_to_vector_collection` to connect to the Astra database and upload data to a vector collection. 
The `connect_to_database` function connects to the Astra database using environment variables for the endpoint 
and token. The `create_or_get_collection` function fetches an existing collection from the database or creates 
a new one if it does not exist. The `upload_csv_to_vector_collection` function uploads in-memory CSV data to 
a vector collection, chunking the data to avoid performance issues.

Author: Team Genz-AI

"""

import os, ast, io
import logging
import pandas as pd
from astrapy import DataAPIClient, Database
from astrapy.constants import VectorMetric
from errors.runtime_error import RuntimeError
from errors.value_error import ValueError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def connect_to_database() -> Database:
    """
    Connects to the Astra database using environment variables for the endpoint and token.

    :return: The connected database instance.
    :raises ValueError: If connection parameters are missing.
    :raises RuntimeError: If connection parameters are missing or any error occurs during connection.
    """
    try:
        endpoint = os.environ.get("ASTRA_DB_API_ENDPOINT")
        token = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")

        if not endpoint or not token:
            raise ValueError(
                "Both ASTRA_DB_API_ENDPOINT and ASTRA_DB_APPLICATION_TOKEN environment variables must be set."
            )

        client = DataAPIClient(token)
        database = client.get_database(endpoint)
        logging.info(f"Successfully connected to database: {database.info().name}")
        return database

    except ValueError as ve:
        logging.error(f"Missing environment variable: {ve}")
        raise ValueError(f"Missing environment variables: {ve}")

    except Exception as e:
        logging.error(f"Error occurred while connecting to the database: {e}")
        raise RuntimeError(
            f"An unexpected error occurred while connecting to the database: {e}"
        )


def create_or_get_collection(database: Database, collection_name: str):
    """
    Fetches an existing collection from the database or creates a new one if it does not exist.

    :param database: The database object where the collection is stored.
    :param collection_name: The name of the collection to fetch or create.
    :raises RuntimeError: If an error occurs while creating the collection.
    :return: The collection object.
    """
    try:
        collection = database.get_collection(collection_name)
        logging.info(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        logging.warning(
            f"Collection '{collection_name}' does not exist. Creating a new one."
        )
        try:
            collection = database.create_collection(
                collection_name, metric=VectorMetric.COSINE
            )
            logging.info(
                f"Created collection '{collection.full_name}' with COSINE metric."
            )
        except Exception as create_error:
            logging.error(
                f"Failed to create collection '{collection_name}': {create_error}"
            )
            raise RuntimeError(
                f"Failed to create collection '{collection_name}': {create_error}"
            )
    return collection


def upload_csv_to_vector_collection(
    collection, csv_data: str, vectorize_column: str, chunk_size: int = 50
):
    """
    Uploads in-memory CSV data to a vector collection, chunking the data to avoid performance issues.

    :param collection: The collection to insert documents into.
    :param csv_data: The in-memory CSV data as a string.
    :param vectorize_column: The name of the column to be used for vectorization.
    :param chunk_size: The size of the chunks to be inserted at once (default is 50).
    :raises ValueError: If the vectorize_column is not found in the CSV data.
    :raises RuntimeError: If an unexpected error occurs during the insertion process.
    """
    try:
        df = pd.read_csv(io.StringIO(csv_data))

        if vectorize_column not in df.columns:
            raise ValueError(f"Column '{vectorize_column}' not found in the CSV data.")

        documents = []
        for _, row in df.iterrows():
            document = row.to_dict()
            document["$vectorize"] = document.pop(vectorize_column)
            document["metadata"] = ast.literal_eval(document["metadata"])
            documents.append(document)

        total_inserted = 0
        for i in range(0, len(documents), chunk_size):
            chunk = documents[i : i + chunk_size]
            try:
                insertion_result = collection.insert_many(chunk, max_time_ms=20000)
                chunk_inserted = len(insertion_result.inserted_ids)
                total_inserted += chunk_inserted
                logging.info(
                    f"Inserted {chunk_inserted} items in chunk {i // chunk_size + 1}."
                )
            except Exception as e:
                logging.error(f"Error inserting chunk {i // chunk_size + 1}: {e}")

        logging.info(
            f"Successfully inserted {total_inserted} items into the collection."
        )

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError(
            f"An unexpected error occurred during the CSV upload process: {e}"
        )
