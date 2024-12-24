import json
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="C:/Users/Trieu/http_ca.crt",  # Replace with your certificate path
    basic_auth=("elastic", "UVNup2ywxoxp6nLJN_Lp")  # Replace with your credentials
)

# Define a search query for Vietnamese text
query = {
    "query": {
        "match": {
            "lyrics": "hãy trao cho anh"
        }
    }
}

# Search the index
result = es.search(index="songs", body=query, size=10)

# Extract and print the title and score
songs = [{"title": hit["_source"]["title"], "score": hit["_score"]} for hit in result["hits"]["hits"]]

# Print results as JSON
print(json.dumps(songs, indent=2, ensure_ascii=False))



