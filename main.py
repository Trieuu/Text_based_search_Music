import time

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

# Initialize Flask app
app = Flask(__name__)

# Connect to Elasticsearch
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
@app.route('/search', methods=['GET'])
def search():
    """
    Perform a search for song titles and lyrics.
    """
    # Get query parameters
    query_text = request.args.get('query', '').strip()
    size = int(request.args.get('size', 10))

    if not query_text:
        return jsonify({"error": "Query parameter 'query' is required"}), 400

    # Elasticsearch query
    query = {
        "query": {
            "bool": {
                "should": [
                    # High-priority exact match for title using `title.raw`
                    {
                        "term": {
                            "title.raw": {
                                "value": query_text,
                                "boost": 15,

                            }
                        }
                    },

                    # High-priority exact match for title with text analysis
                    {
                        "match": {
                            "title": {
                                "query": query_text,
                                "fuzziness": "0",
                                "boost": 10,
                                "minimum_should_match": "60%"
                            }
                        }
                    },

                    # Medium-priority fuzzy match for title
                    {
                        "match": {
                            "title": {
                                "query": query_text,
                                "fuzziness": "AUTO",
                                "boost": 5
                            }
                        }
                    },

                    # Low-priority match for lyrics
                    {
                        "match": {
                            "lyrics": {
                                "query": query_text,
                                "fuzziness": "AUTO",
                                "boost": 1,
                            }
                        }
                    },
                    # Slightly boosted exact match for lyrics
                    {
                        "match": {
                            "lyrics": {
                                "query": query_text,
                                "fuzziness": "0",
                                "boost": 8,
                                "minimum_should_match": "60%"

                            }
                        }
                    },

                ]
            }
        }
    }

    try:
        # Perform the search
        result = es.search(index="songs", body=query, size=size)

        # Process the results and remove duplicates
        final_results = []
        seen_titles = set()

        for hit in result["hits"]["hits"]:
            title = hit["_source"]["title"]
            score = hit["_score"]
            official_link = hit["_source"].get("official_link", "Not Found")
            # Add the result, avoiding duplicates
            if title not in seen_titles:
                final_results.append({
                    "title": title,
                    "score": score,
                    "link": official_link,# Include the first 100 characters of lyrics
                })
                seen_titles.add(title)

        # Sort results by score in descending order
        sorted_results = sorted(final_results, key=lambda x: x["score"], reverse=True)

        return jsonify(sorted_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/favicon.ico')
def favicon():
    """
    Handle requests for favicon.ico to avoid 404 errors.
    """
    return '', 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

