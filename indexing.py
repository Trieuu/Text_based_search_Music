from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="C:/Users/Trieu/http_ca.crt",  # Replace with your certificate path
    basic_auth=("elastic", "UVNup2ywxoxp6nLJN_Lp")  # Replace with your credentials
)

# Use the recommended `.options()` method and updated syntax
es = es.options(ignore_status=400)  # Ignore the error if the index already exists

# Create the index with updated mapping
es.indices.create(
    index="songs",
    body={
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "vi_analyzer",
                    "fields": {
                        "raw": {
                            "type": "keyword"  # For exact matches
                        }
                    }
                },
                "lyrics": {
                    "type": "text",
                    "analyzer": "vi_analyzer"
                }
            }
        },
        "settings": {
            "analysis": {
                "analyzer": {
                    "vi_analyzer": {
                        "type": "custom",
                        "tokenizer": "icu_tokenizer",
                        "filter": ["lowercase", "icu_folding"]
                    }
                }
            }
        }
    }
)

print("Index created successfully (or already exists).")



