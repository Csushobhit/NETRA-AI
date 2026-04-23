from db.opensearch_client import get_client

client = get_client()

INDICES = [
    "maltrail_ips",
    "known_malicious_ips",
    "known_risky_ips",
    "known_low_risky_ips",
    "known_unknown_ips"
]

def get_all_ips(index, page=1, size=50, search_ip=None):
    if index not in INDICES:
        return []

    start = (page - 1) * size

    query = {"match_all": {}}

    if search_ip:
        query = {
            "wildcard": {
                "_id": f"*{search_ip}*"
            }
        }

    res = client.search(
        index=index,
        body={
            "from": start,
            "size": size,
            "query": query
        }
    )

    return [
        {
            "ip": hit["_id"],
            "source": index
        }
        for hit in res["hits"]["hits"]
    ]


def delete_ip(index, ip):
    if index not in INDICES:
        return False

    if not client.exists(index=index, id=ip):
        return False

    client.delete(index=index, id=ip)
    return True