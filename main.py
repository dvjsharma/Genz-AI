"""
Brief: This file contains the functions to query a vector search API and return the response.

Description: This file contains the function `process_query` to process the query by fetching data, 
uploading it to a vector database, and performing a vector search. The function interacts with the 
user via the command line to input the Instagram user ID and the query string. It then calls the 
`fetch_data` function to fetch data, uploads the data to a vector database, and performs a vector 
search using the specified query. The extracted answer is displayed to the user along with the full 
response.

Author: Team Genz-AI

"""

import os
from services.instagram_service import fetch_data
from services.db_service import (
    connect_to_database,
    create_or_get_collection,
    upload_csv_to_vector_collection,
)
from services.search_service import vector_search


def process_query(instagram_id: str, query: str):
    """
    Perform a vector search using the specified query message.

    :param query_message: The input message to query the vector search.
    :type query_message: str
    :return: A tuple containing the full JSON response and the extracted answer.
    :rtype: tuple
    :raises RuntimeError: If the vector search fails or the response format is invalid.
    """

    csv = fetch_data(instagram_id)

    database = connect_to_database()
    collection_name = os.environ.get("ASTRA_DB_COLLECTION_NAME")
    collection = create_or_get_collection(database, collection_name)

    upload_csv_to_vector_collection(collection, csv, "vectorize")
    response = vector_search(query)
    message = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]

    return response, message


def main():
    """
    Main function to interact with the user via the command line.
    """
    instagram_id = input("Enter the Instagram user ID: ")
    query = input("Enter the query string: ")

    try:
        response, message = process_query(instagram_id, query)
        print("\n--- Results ---")
        print("Full Response:", response)
        print("Extracted Answer:", message)
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
