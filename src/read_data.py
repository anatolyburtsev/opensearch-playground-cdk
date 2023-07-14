import json

from src.OpenSearchClient import OSClient
import random
from timeit import default_timer as timer


def generate_unique_randoms(num_unique, range_max):
    numbers = set()

    while len(numbers) < num_unique:
        num = random.randint(1, range_max)
        numbers.add(num)

    return list(numbers)


def measure_time(number_of_docs):
    doc_ids = generate_unique_randoms(number_of_docs, 500000)

    for i in [1, 2, 5, 10, 20, 50, 100]:
        start = timer()
        docs = os_client.search_multiple_docs(doc_ids, i)
        end = timer()
        print(f"num_threads = {i:02d}, time: {end - start:.2f} secs")

    start = timer()
    response = os_client.search_multiple_docs_in_bulk(doc_ids)
    end = timer()
    print(f"Multiple search. time: {end - start:.2f} secs")


if __name__ == "__main__":
    os_url = "search-open-search-hello-world-ptsefi3fh6osw2up7h6mq3ai3a.us-east-1.es.amazonaws.com"
    index_name = "food-reviews-index"
    os_client = OSClient(os_url, index_name)

    for doc_number in [100, 1000, 10000, 30000]:
        print(f"number of docs to search: {doc_number}")
        measure_time(doc_number)
