import time

from elasticsearch import Elasticsearch

es = None
for _ in range(10):  # Retry up to 10 times
    try:
        es = Elasticsearch(hosts=["http://elasticsearch:9200"],)
        if es.ping():
            print("Connected to Elasticsearch")
            break
    except Exception as e:
        print("Waiting for Elasticsearch...", e)
        time.sleep(5)  # Wait for 5 seconds before retrying
else:
    raise ConnectionError("Elasticsearch is not available")
# Use the recommended `.options()` method and updated syntax
#es = es.options(ignore_status=400)  # Ignore the error if the index already exists

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
            },
            "official_link": {
                "type": "keyword"  # Store URLs as exact values without tokenization
            }
        }
    }
}

# Create the index
response = es.indices.create(index="songs", body=index_body)

print("Index creation response:", response)

print("Index created successfully (or already exists).")



