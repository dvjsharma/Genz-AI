import os

from services.instagram_service import fetch_data
from services.db_service import connect_to_database, create_or_get_collection, upload_csv_to_vector_collection
from services.search_service import vector_search
csv = fetch_data("sergi_gsxs")
database = connect_to_database()
collection = create_or_get_collection(database, os.environ.get("ASTRA_DB_COLLECTION_NAME"))
upload_csv_to_vector_collection(collection, csv, "vectorize")
res = vector_search("What is the maximum likes count in static-image post type")
ans = res.outputs[0].outputs[0].results.message.data.text.strip()
print(ans)
# print(csv)