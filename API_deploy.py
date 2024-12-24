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
        query_text = request.form.get('query', '')
        size = int(request.form.get('size', 10))

        # Define a bool query to score both title and lyrics, prioritizing title with a higher boost
        query = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"title": {"query": query_text, "fuzziness": "AUTO", "boost": 2}}},  # Boost title
                        {"match": {"lyrics": {"query": query_text, "fuzziness": "AUTO", "boost": 1}}}   # Lower priority for lyrics
                    ]
                }
            }
        }

        # Perform the search
        result = es.search(index="songs", body=query, size=size)

        # Deduplicate results: First prioritize titles, then include lyrics
        seen_titles = set()  # To avoid duplicate titles
        songs = []

        for hit in result["hits"]["hits"]:
            title = hit["_source"]["title"]
            score = hit["_score"]

            # If it's a title match
            if "title" in hit["_source"]:
                if title not in seen_titles:
                    songs.append({"match_type": f"title: {title}", "score": score})
                    seen_titles.add(title)
            # If it's a lyrics match
            elif "lyrics" in hit["_source"]:
                if title not in seen_titles:
                    songs.append({"match_type": f"lyrics: {title}", "score": score})
                    seen_titles.add(title)

        # Pass the results back to the HTML page
        return render_template('index.html', results=songs, query_text=query_text, size=size)

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




