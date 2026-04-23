from db.opensearch_client import get_client

client = get_client()

def exists(index, ip):
    res = client.search(
        index=index,
        body={"query": {"match": {"ip": ip}}},
        size=1
    )
    return len(res["hits"]["hits"]) > 0

def store(index, ip, score=None, source=None):
    doc = {
        "ip": ip,
        "score": score,
        "source": source
    }
    client.index(index=index, body=doc)