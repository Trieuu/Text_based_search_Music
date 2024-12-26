from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

# Initialize Flask app
app = Flask(__name__)

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="F:/Text_based_search_Music/http_ca.crt",  # Replace with your certificate path
    basic_auth=("elastic", "T-5=Edh3P*1Q*=Imo1_0")  # Replace with your credentials
)

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
                                "boost": 15  # Very high boost for exact title match
                            }
                        }
                    },
                    # High-priority exact match for title with text analysis
                    {
                        "match": {
                            "title": {
                                "query": query_text,
                                "fuzziness": "0",
                                "boost": 10
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
                                "boost": 1
                            }
                        }
                    },
                    # Slightly boosted exact match for lyrics
                    {
                        "match": {
                            "lyrics": {
                                "query": query_text,
                                "fuzziness": "0",
                                "boost": 5
                            }
                        }
                    }
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

            # Add the result, avoiding duplicates
            if title not in seen_titles:
                final_results.append({
                    "title": title,
                    "score": score,
                    "snippet": hit["_source"].get("lyrics", "")[:100]  # Include the first 100 characters of lyrics
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
    app.run(debug=True)

