from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import logging
from services.instagram_service import fetch_data
from services.db_service import (
    connect_to_database,
    create_or_get_collection,
    upload_csv_to_vector_collection,
)
from services.search_service import vector_search
from errors.runtime_error import RuntimeError
from errors.value_error import ValueError

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

@app.route("/process_data", methods=["POST"])
def process_data_api():
    """
    API to process Instagram user data and upload it to the vector database.
    
    Request JSON Body:
    {
        "instagram_id": "<Instagram User ID>"
    }

    Response:
    {
        "message": "Data processed successfully for Instagram ID <id>."
    }
    """
    try:
        data = request.json
        instagram_id = data.get("instagram_id")

        if not instagram_id:
            return jsonify({"error": "Instagram ID is required."}), 400

        collection_name = os.environ.get("ASTRA_DB_COLLECTION_NAME")
        if not collection_name:
            raise ValueError("ASTRA_DB_COLLECTION_NAME environment variable is not set.")

        database = connect_to_database()
        collection = create_or_get_collection(database, collection_name)
        csv = fetch_data(instagram_id)
        upload_csv_to_vector_collection(collection, csv, "vectorize")

        return jsonify({"message": f"Data processed successfully for Instagram ID {instagram_id}."}), 200

    except ValueError as ve:
        logging.error(str(ve))
        return jsonify({"error": str(ve)}), 400
    except RuntimeError as re:
        logging.error(str(re))
        return jsonify({"error": str(re)}), 500
    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@app.route("/process_query", methods=["POST"])
def process_query_api():
    """
    API to perform a vector search using a query string.
    
    Request JSON Body:
    {
        "query": "<Query String>"
    }

    Response:
    {
        "response": <Full Response JSON>,
        "message": "<Extracted Answer>"
    }
    """
    try:
        data = request.json
        query = data.get("query")

        if not query:
            return jsonify({"error": "Query string is required."}), 400

        response = vector_search(query)
        message = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]

        if not message:
            raise RuntimeError("The response format is invalid or does not contain the expected 'message' field.")

        return jsonify({"response": response, "message": message}), 200

    except ValueError as ve:
        logging.error(str(ve))
        return jsonify({"error": str(ve)}), 400
    except RuntimeError as re:
        logging.error(str(re))
        return jsonify({"error": str(re)}), 500
    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True)
