from db.opensearch_client import get_client
from memory.normalizer import normalize

client = get_client()
INDEX = "memory"


def get_similar(feature):
    vector = normalize(feature)

    query = {
        "size": 3,
        "query": {
            "bool": {
                "must": [
                    {
                        "knn": {
                            "feature_vector": {
                                "vector": vector,
                                "k": 3
                            }
                        }
                    }
                ],
                "must_not": [
                    {
                        "term": {
                            "feedback": "incorrect"
                        }
                    }
                ]
            }
        }
    }

    res = client.search(index=INDEX, body=query)

    return [hit["_source"] for hit in res["hits"]["hits"]]