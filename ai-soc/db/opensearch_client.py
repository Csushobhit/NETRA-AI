from opensearchpy import OpenSearch

def get_client():
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "DEep@5515"),
        use_ssl=False,
        verify_certs=False
    )
    return client