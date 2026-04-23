from db.opensearch_client import get_client

client = get_client()


def create_indices():
    indices = {
        "maltrail_ips": {
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "status": {"type": "keyword"},
                    "source": {"type": "keyword"}
                }
            }
        },
        "known_malicious_ips": {
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "score": {"type": "float"},
                    "source": {"type": "keyword"}
                }
            }
        },
        "known_risky_ips": {
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "score": {"type": "float"},
                    "source": {"type": "keyword"}
                }
            }
        },
        "known_low_risky_ips": {
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "score": {"type": "float"},
                    "source": {"type": "keyword"}
                }
            }
        },
        "known_unknown_ips": {
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "score": {"type": "float"},
                    "source": {"type": "keyword"}
                }
            }
        },
        "logs": {
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "timestamp": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss"
                    },
                    "event_type": {"type": "keyword"},
                    "status": {"type": "keyword"},
                    "port": {"type": "integer"}
                }
            }
        },
        "memory": {
            "settings": {
                "index": {
                    "knn": True
                }
            },
            "mappings": {
                "properties": {
                    "ip": {"type": "ip"},
                    "feature_vector": {
                        "type": "knn_vector",
                        "dimension": 4
                    },
                    "request_freq": {"type": "float"},
                    "failed_ratio": {"type": "float"},
                    "unique_ports": {"type": "integer"},
                    "off_hour": {"type": "integer"},
                    "decision": {"type": "keyword"},
                    "risk": {"type": "float"},
                    "feedback": {"type": "keyword"}
                }
            }
        }
    }

    for idx, body in indices.items():
        if not client.indices.exists(index=idx):
            client.indices.create(index=idx, body=body)
            print(f"Created: {idx}")
        else:
            print(f"Exists: {idx}")


if __name__ == "__main__":
    create_indices()