import json

from src.OpenSearchClient import OSClient
from src.read_data import generate_unique_randoms


def list_to_set(list1):
    return set(json.dumps(item, sort_keys=True) for item in list1)


def compare_2_lists(list1, list2):
    set1 = list_to_set(list1)
    set2 = list_to_set(list2)

    return set1 == set2


if __name__ == "__main__":
    os_url = "search-open-search-hello-world-ptsefi3fh6osw2up7h6mq3ai3a.us-east-1.es.amazonaws.com"
    index_name = "food-reviews-index"
    os_client = OSClient(os_url, index_name)
    doc_ids = generate_unique_randoms(1000, 500000)

    docs = os_client.search_multiple_docs(doc_ids, 100)
    docs2 = os_client.search_multiple_docs_in_bulk(doc_ids)
    print(f"Are docs the same?: {compare_2_lists(docs, docs2)}")
    print(f"doc sample: {docs[0]}")
