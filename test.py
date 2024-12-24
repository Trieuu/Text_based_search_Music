from elasticsearch import Elasticsearch

# Connect to Elasticsearch with HTTPS and authentication
es = Elasticsearch(
    "https://localhost:9200",
    # docker cp gracious_lumiere:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt
    ca_certs="C:/Users/Trieu/http_ca.crt",  # Replace with the actual path to your certificate
    # docker exec -it gracious_lumiere bin/elasticsearch-reset-password -u elastic
    basic_auth=("elastic", "UVNup2ywxoxp6nLJN_Lp")  # Replace with the actual password
)

# Test connection
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

