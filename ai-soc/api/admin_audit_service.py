from db.opensearch_client import get_client
from datetime import datetime

client = get_client()
INDEX = "admin_audit_logs"

def log_action(action, ip, index, status):
    doc = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "ip": ip,
        "index": index,
        "status": status
    }

    client.index(index=INDEX, body=doc)


def get_logs(page=1, size=20):
    start = (page - 1) * size

    res = client.search(
        index=INDEX,
        body={
            "from": start,
            "size": size,
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {"match_all": {}}
        }
    )

    return [hit["_source"] for hit in res["hits"]["hits"]]