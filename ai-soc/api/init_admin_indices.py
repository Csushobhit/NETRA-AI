from db.opensearch_client import get_client

client = get_client()
AUDIT_INDEX = "admin_audit_logs"

def create_audit_index():
    if client.indices.exists(index=AUDIT_INDEX):
        return

    mapping = {
        "mappings": {
            "properties": {
                "timestamp": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "action": {"type": "keyword"},
                "ip": {"type": "keyword"},
                "index": {"type": "keyword"},
                "status": {"type": "keyword"}
            }
        }
    }

    client.indices.create(index=AUDIT_INDEX, body=mapping)