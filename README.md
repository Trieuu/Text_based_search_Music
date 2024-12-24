__PLease read this one before doing anything__

Step by step to run the project:

0. Download Docker and register, you will get some a name like: 'gracious_lumiere' in the Containers

1. Before running any .py file, please run the following command in the cmd:
- 'docker cp gracious_lumiere:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt'
  -- After running this, you will get thing like: Successfully copied 3.58kB to C:\Users\Trieu\http_ca.crt
- 'docker exec -it gracious_lumiere bin/elasticsearch-reset-password -u elastic'
  -- After running this, you will get thing like: New value: UVNup2ywxoxp6nLJN_Lp

2. Then, in each .py file that conatin:
es = Elasticsearch(
    "https://localhost:9200",
    \# docker cp gracious_lumiere:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt
    ca_certs="C:/Users/Trieu/http_ca.crt",  # Replace with your certificate path
    \# docker exec -it gracious_lumiere bin/elasticsearch-reset-password -u elastic
    basic_auth=("elastic", "UVNup2ywxoxp6nLJN_Lp")  # Replace with your credentials
)
Please change all the things you get in step 1 to the 'ca_certs' and 'basic_auth' to match your version.

3. Run as with this order the file:
- indexing.py
- load_index_to_elastic.py
- API_deploy_2.py

4. You will get the link in the output like: 'http://127.0.0.1:5000' .That is all the thing!
