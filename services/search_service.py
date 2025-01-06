"""
Brief: This file contains the functions to query a vector search API and return the response.

Description: This file contains the function `vector_search` to perform a vector search using 
the specified query message. The function sends a POST request to the vector search API (langflow) 
with the input message and returns the JSON response. It also handles errors related to missing 
environment variables and API request failures.

Author: Team Genz-AI

"""

import os
import requests
import logging
from errors.runtime_error import RuntimeError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def vector_search(query_message: str) -> dict:
    """
    Perform a vector search using the specified query message.

    :param query_message: The input message to query the vector search.
    :return: The JSON response from the vector search API.
    :raises RuntimeError: If the environment variables are not properly set or the API request fails.
    """
    try:
        base_api_url = os.environ.get("BASE_API_URL")
        langflow_id = os.environ.get("LANGFLOW_ID")
        endpoint = os.environ.get("ENDPOINT")
        application_token = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")

        if not (base_api_url and langflow_id and endpoint and application_token):
            raise RuntimeError(
                "Please ensure BASE_API_URL, LANGFLOW_ID, ENDPOINT, and ASTRA_DB_APPLICATION_TOKEN are set as environment variables."
            )

        api_url = f"{base_api_url}/lf/{langflow_id}/api/v1/run/{endpoint}"

        payload = {
            "input_value": query_message,
            "output_type": "chat",
            "input_type": "chat",
        }
        headers = {
            "Authorization": f"Bearer {application_token}",
            "Content-Type": "application/json",
        }

        logging.info(f"Sending vector search request to: {api_url}")
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()

        logging.info("Vector search request successful.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise RuntimeError(f"An error occurred while performing the vector search: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError(f"An unexpected error occurred: {e}")
