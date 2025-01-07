"""
Brief: This file contains the main function to interact with the user via the command line.

Description: This file contains the main function to interact with the user via the command line. 
The user is prompted to enter an Instagram user ID and a query string. The data for the Instagram 
user is fetched and uploaded to a vector database. The query string is used to perform a vector 
search, and the full response and the extracted answer are displayed to the user.

Author: Team Genz-AI
``
"""

import os
import logging
from dotenv import load_dotenv
from services.instagram_service import fetch_data
from services.db_service import (
    connect_to_database,
    create_or_get_collection,
    upload_csv_to_vector_collection,
)
from services.search_service import vector_search
from errors.runtime_error import RuntimeError
from errors.value_error import ValueError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_data(instagram_id: str):
    """
    Fetch data for a given Instagram user and upload it to a vector database.

    :param instagram_id: The Instagram user ID for which data is to be fetched.
    :return: A message indicating the success of the data upload operation.
    :raises ValueError: If the `ASTRA_DB_COLLECTION_NAME` environment variable is not set.
    :raises RuntimeError: If data upload fails.
    """
    collection_name = os.environ.get("ASTRA_DB_COLLECTION_NAME")
    if not collection_name:
        raise ValueError("ASTRA_DB_COLLECTION_NAME environment variable is not set.")

    try:
        database = connect_to_database()
        collection = create_or_get_collection(database, collection_name)
        csv = fetch_data(instagram_id)
        upload_csv_to_vector_collection(collection, csv, "vectorize")
    except Exception as e:
        raise RuntimeError(f"An error occurred during data upload: {str(e)}") from e


def process_query(query: str):
    """
    Perform a vector search using the specified query message.

    :param query: The input message for the vector search.
    :return: A tuple containing the full JSON response and the extracted answer.
    :raises ValueError: If the query is empty or invalid.
    :raises RuntimeError: If the vector search fails or the response format is invalid.
    """
    if not query or not isinstance(query, str):
        raise ValueError("The query must be a non-empty string.")

    try:
        response = vector_search(query)
        message = response["outputs"][0]["outputs"][0]["results"]["message"]["data"][
            "text"
        ]

        if not message:
            raise RuntimeError(
                "The response format is invalid or does not contain the expected 'message' field."
            )

        return response, message
    except KeyError as e:
        raise RuntimeError(f"Missing expected key in the response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"An error occurred during vector search: {str(e)}") from e


def main():
    """
    Main function to interact with the user via the command line.
    """
    load_dotenv()
    instagram_id = input("Enter the Instagram user ID: ")
    query = input("Enter the query string: ")

    try:
        process_data(instagram_id)
        response, message = process_query(query)
        print("\n--- Results ---")
        print("Full Response:", response)
        print("Extracted Answer:", message)
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
