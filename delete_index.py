import json
from elasticsearch import Elasticsearch

# Connect to Elasticsearch


es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="F:/Text_based_search_Music/http_ca.crt",  # Replace with your certificate path
    basic_auth=("elastic", "T-5=Edh3P*1Q*=Imo1_0")  # Replace with your credentials
)
# mapping = es.indices.get_mapping(index="songs").body
# import json
# print(json.dumps(mapping, indent=2))

# Delete the "songs" index
es.indices.delete(index="songs", ignore=[400, 404])

print("Index 'songs' deleted successfully (if it existed).")

