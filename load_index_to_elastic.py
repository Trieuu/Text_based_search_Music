import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="C:/Users/Trieu/http_ca.crt",  # Replace with your certificate path
    basic_auth=("elastic", "UVNup2ywxoxp6nLJN_Lp")  # Replace with your credentials
)

# Load the JSON data
with open("data_with_lyrics.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare the data for bulk indexing
actions = [
    {
        "_index": "songs",
        "_id": f"{item['name']}_{hash(item['lyrics'])}",  # Generate a unique _id using title and lyrics hash
        "_source": {
            "title": item["name"],
            "lyrics": item["lyrics"]
        }
    }
    for item in data
]

# Bulk index the data
success, _ = bulk(es, actions)
print(f"Successfully indexed {success} documents.")


