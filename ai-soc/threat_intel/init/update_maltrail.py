import os
import re
import subprocess
from opensearchpy import helpers
from db.opensearch_client import get_client

client = get_client()

LOCAL_PATH = "maltrail"
BASE_PATH = os.path.join(LOCAL_PATH, "trails", "static")


def update_repo():
    if os.path.exists(LOCAL_PATH):
        print("Pulling latest updates...")
        subprocess.run(["git", "-C", LOCAL_PATH, "pull"])
    else:
        print("Maltrail not found. Run loader first.")
        return False
    return True



def extract_ips(file_path):
    pattern = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
    ips = []

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            ips.extend(re.findall(pattern, line))

    return ips


def get_existing_ips():
    print("Fetching existing IPs from OpenSearch...")

    existing = set()

    query = {
        "query": {"match_all": {}},
        "_source": False
    }

    resp = client.search(
        index="maltrail_ips",
        body=query,
        scroll="2m",
        size=10000
    )

    scroll_id = resp["_scroll_id"]
    hits = resp["hits"]["hits"]

    while hits:
        for h in hits:
            existing.add(h["_id"])

        resp = client.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = resp["_scroll_id"]
        hits = resp["hits"]["hits"]

    print(f"Loaded {len(existing)} existing IPs")
    return existing



def update():
    if not update_repo():
        return

    existing_ips = get_existing_ips()

    actions = []
    BATCH_SIZE = 5000
    new_count = 0

    print("Processing files...")

    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            path = os.path.join(root, file)
            ips = extract_ips(path)

            for ip in ips:
                if ip not in existing_ips:
                    actions.append({
                        "_index": "maltrail_ips",
                        "_id": ip,
                        "_source": {
                            "ip": ip,
                            "status": "malicious",
                            "source": "maltrail"
                        }
                    })

                    existing_ips.add(ip)  # prevent duplicates in same run
                    new_count += 1

                if len(actions) >= BATCH_SIZE:
                    helpers.bulk(client, actions)
                    actions = []

    # final flush
    if actions:
        helpers.bulk(client, actions)

    print(f"New IPs added: {new_count}")




if __name__ == "__main__":
    update()