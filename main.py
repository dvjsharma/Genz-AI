import os

from services.instagram_service import fetch_data
from services.db_service import connect_to_database, create_or_get_collection, upload_csv_to_vector_collection
csv = fetch_data("sergi_gsxs")
database = connect_to_database()
collection = create_or_get_collection(database, os.environ.get("COLLECTION_NAME"))
upload_csv_to_vector_collection(collection, csv, "vectorize")
# print(csv)