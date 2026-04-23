from db.opensearch_client import get_client

INDEX = "logs"

client = get_client()

def init_file():
    if not client.indices.exists(index=INDEX):
        client.indices.create(index=INDEX)

def write_log(log):
    client.index(index=INDEX, body=log)