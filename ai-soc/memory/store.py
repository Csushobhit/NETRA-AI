from db.opensearch_client import get_client

client = get_client()
INDEX = "memory"


def save_record(record):
    client.index(
        index=INDEX,
        body=record
    )


def update_feedback(ip, feedback):
    query = {
        "query": {
            "term": {
                "ip": ip
            }
        },
        "size": 1,
        "sort": [
            {"_id": {"order": "desc"}}
        ]
    }

    res = client.search(index=INDEX, body=query)

    hits = res["hits"]["hits"]

    if not hits:
        return

    doc_id = hits[0]["_id"]

    client.update(
        index=INDEX,
        id=doc_id,
        body={
            "doc": {
                "feedback": feedback
            }
        }
    )