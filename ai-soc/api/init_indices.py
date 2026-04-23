from db.opensearch_client import get_client

client = get_client()

INDEX = "alerts"

def create_alert_index():
    if client.indices.exists(index=INDEX):
        return

    mapping = {
        "mappings": {
            "properties": {
                "ip": {"type": "keyword"},
                "window": {"type": "long"},
                "timestamp": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "request_freq": {"type": "integer"},
                "failed_ratio": {"type": "float"},
                "unique_ports": {"type": "integer"},
                "off_hour": {"type": "integer"},
                "anomaly_score": {"type": "float"},
                "attack_type": {"type": "keyword"},
                "risk_score": {"type": "integer"},
                "action": {"type": "keyword"},
                "explanation": {"type": "text"},
                "ti_label": {"type": "keyword"},
                "ti_confidence": {"type": "integer"},
                "ti_reasoning": {"type": "text"}
            }
        }
    }

    client.indices.create(index=INDEX, body=mapping)