from opensearchpy import helpers
import os
import re
import subprocess
from db.opensearch_client import get_client

client = get_client()

REPO_URL = "https://github.com/stamparm/maltrail.git"
LOCAL_PATH = "maltrail"
BASE_PATH = os.path.join(LOCAL_PATH, "trails", "static")


def clone_repo():
    if not os.path.exists(LOCAL_PATH):
        subprocess.run(["git", "clone", REPO_URL])


def extract_ips(file_path):
    pattern = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
    ips = []

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            ips.extend(re.findall(pattern, line))

    return ips


def load():
    clone_repo()

    actions = []
    BATCH_SIZE = 6000

    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            path = os.path.join(root, file)
            ips = extract_ips(path)

            for ip in ips:
                actions.append({
                    "_index": "maltrail_ips",
                    "_id": ip,
                    "_source": {
                        "ip": ip,
                        "status": "malicious",
                        "source": "maltrail"
                    }
                })

                if len(actions) >= BATCH_SIZE:
                    helpers.bulk(client, actions)
                    actions = []

    if actions:
        helpers.bulk(client, actions)

    print("FAST load complete")


if __name__ == "__main__":
    load()