from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="F:/Text_based_search_Music/http_ca.crt",  # Replace with your certificate path
    basic_auth=("elastic", "T-5=Edh3P*1Q*=Imo1_0")  # Replace with your credentials
)

# Use the recommended `.options()` method and updated syntax
es = es.options(ignore_status=400)  # Ignore the error if the index already exists

# Create the index with updated mapping
index_body = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "kuromoji_user_dict": {
                    "type": "kuromoji_tokenizer"
                }
            },
            "filter": {
                "kuromoji_baseform": {
                    "type": "kuromoji_baseform"
                },
                "kuromoji_part_of_speech": {
                    "type": "kuromoji_part_of_speech"
                },
                "cjk_width": {
                    "type": "cjk_width"
                },
                "kuromoji_stemmer": {
                    "type": "kuromoji_stemmer"
                },
                "lowercase": {
                    "type": "lowercase"
                },
                "icu_folding": {
                    "type": "icu_folding"
                }
            },
            "analyzer": {
                "vi_analyzer": {
                    "type": "custom",
                    "tokenizer": "icu_tokenizer",
                    "filter": ["lowercase", "icu_folding"]
                },
                "english_analyzer": {
                    "type": "standard"
                },
                "japanese_analyzer": {
                    "type": "custom",
                    "tokenizer": "kuromoji_user_dict",
                    "filter": [
                        "kuromoji_baseform",
                        "kuromoji_part_of_speech",
                        "cjk_width",
                        "kuromoji_stemmer",
                        "lowercase"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title": {
                "type": "text",
                "fields": {
                    "raw": {
                        "type": "keyword"  # For exact matches
                    }
                },
                "analyzer": "english_analyzer"
            },
            "lyrics_vi": {
                "type": "text",
                "analyzer": "vi_analyzer"
            },
            "lyrics_en": {
                "type": "text",
                "analyzer": "english_analyzer"
            },
            "lyrics_ja": {
                "type": "text",
                "analyzer": "japanese_analyzer"
            }
        }
    }
}

# Create the index
response = es.indices.create(index="songs", body=index_body)

print("Index creation response:", response)

print("Index created successfully (or already exists).")



