import json
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = None
for _ in range(10):  # Retry up to 10 times
    try:
        es = Elasticsearch(hosts=["http://elasticsearch:9200"])
        if es.ping():
            print("Connected to Elasticsearch")
            break
    except Exception as e:
        print("Waiting for Elasticsearch...", e)
        time.sleep(5)  # Wait for 5 seconds before retrying
else:
    raise ConnectionError("Elasticsearch is not available")
# Load the JSON data
with open("data_with_lyrics_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare the data for bulk indexing
actions = [
    {
        "_index": "songs",
        "_id": f"{item['name']}_{hash(item['lyrics'])}",  # Generate a unique _id using title and lyrics hash
        "_source": {
            "title": item["name"],
            "lyrics": item["lyrics"],
            "official_link": item["official_link"],

        }
    }
    for item in data
]

# Bulk index the data
success, _ = bulk(es, actions)
print(f"Successfully indexed {success} documents.")


