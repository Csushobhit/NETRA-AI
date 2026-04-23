from db.opensearch_client import get_client

client = get_client()
INDEX = "alerts"

def generate_id(ip, window):
    return f"{ip}_{window}"

def store_alert(alert):
    doc_id = generate_id(alert["ip"], alert["window"])

    if client.exists(index=INDEX, id=doc_id):
        return

    client.index(index=INDEX, id=doc_id, body=alert)

def get_alerts(filter_type=None, hours=None):
    query = {"match_all": {}}

    if filter_type == "suspicious":
        query = {"range": {"risk_score": {"gte": 50}}}

    if hours:
        query = {
            "bool": {
                "must": [
                    {"range": {"timestamp": {"gte": f"now-{hours}h"}}}
                ]
            }
        }

    res = client.search(
        index=INDEX,
        body={
            "query": query,
            "size": 1000,
            "sort": [
                {"timestamp": {"order": "desc"}}
            ]
        }
    )

    return [h["_source"] for h in res["hits"]["hits"]]

def get_by_ip(ip):
    query = {"term": {"ip": ip}}

    res = client.search(
        index=INDEX,
        body={
            "query": query,
            "size": 50,
            "sort": [
                {"timestamp": {"order": "desc"}}
            ]
        }
    )

    return [h["_source"] for h in res["hits"]["hits"]]

def update_ti(ip, label, confidence, reasoning):
    query = {"term": {"ip": ip}}

    res = client.search(
        index=INDEX,
        body={
            "query": query,
            "size": 1
        }
    )

    if not res["hits"]["hits"]:
        return

    doc_id = res["hits"]["hits"][0]["_id"]

    client.update(
        index=INDEX,
        id=doc_id,
        body={
            "doc": {
                "ti_label": label,
                "ti_confidence": confidence,
                "ti_reasoning": reasoning
            }
        }
    )