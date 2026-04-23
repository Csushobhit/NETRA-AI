from db.opensearch_client import get_client

INDEX = "logs"

client = get_client()

def read_new_logs(last_timestamp):
    query = {
        "query": {
            "range": {
                "timestamp": {
                    "gt": last_timestamp
                }
            }
        },
        "size": 1000,
        "sort": [
            {"timestamp": {"order": "asc"}}
        ]
    }

    res = client.search(index=INDEX, body=query)

    hits = res["hits"]["hits"]

    logs = [hit["_source"] for hit in hits]

    if logs:
        new_timestamp = logs[-1]["timestamp"]
    else:
        new_timestamp = last_timestamp

    return logs, new_timestamp