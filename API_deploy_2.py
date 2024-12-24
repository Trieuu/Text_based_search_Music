from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch

# Initialize Flask app
app = Flask(__name__)

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    # docker cp gracious_lumiere:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt
    ca_certs="C:/Users/Trieu/http_ca.crt",  # Replace with your certificate path
    # docker exec -it gracious_lumiere bin/elasticsearch-reset-password -u elastic
    basic_auth=("elastic", "UVNup2ywxoxp6nLJN_Lp")  # Replace with your credentials
)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render the home page with a form to input song query and size.
    """
    if request.method == 'POST':
        # Get form inputs
        query_text = request.form.get('query', '').strip()
        size = int(request.form.get('size', 10))

        # Perform the search for both title and lyrics, prioritizing title matches
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
                        }
                    ]
                }
            }
        }


        # Search using the query
        result = es.search(index="songs", body=query, size=size)

        # Process the results and ensure no duplicates
        final_results = []
        seen_titles = set()

        for hit in result["hits"]["hits"]:
            title = hit["_source"]["title"]
            score = hit["_score"]

            # Add the result, prioritizing unique titles
            if title not in seen_titles:
                final_results.append({"match_type": f"title: {title}", "score": score})
                seen_titles.add(title)

            # Perform a secondary search using the title to find matching lyrics
            title_query = {
                "query": {
                    "match": {
                        "lyrics": {"query": title, "fuzziness": "AUTO"}
                    }
                }
            }
            title_search_result = es.search(index="songs", body=title_query, size=size)

            for lyric_hit in title_search_result["hits"]["hits"]:
                lyric_title = lyric_hit["_source"]["title"]
                lyric_score = lyric_hit["_score"]

                # Avoid duplicate matches
                if lyric_title not in seen_titles:
                    final_results.append({"match_type": f"lyrics: {lyric_title}", "score": lyric_score})
                    seen_titles.add(lyric_title)

        # Sort results by score in descending order
        sorted_results = sorted(final_results, key=lambda x: x["score"], reverse=True)

        # Pass the sorted results back to the HTML page
        return render_template('index.html', results=sorted_results, query_text=query_text, size=size)

    # Render the initial page
    return render_template('index.html', results=None)

@app.route('/favicon.ico')
def favicon():
    """
    Handle requests for favicon.ico to avoid 404 errors.
    """
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
