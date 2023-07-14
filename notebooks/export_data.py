import csv
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import json
from tqdm import tqdm
import math
import time
from time import perf_counter


class OSClient:
    def __init__(self, url, region="us-east-1"):
        service = "es"
        credentials = boto3.Session().get_credentials()
        auth = AWSV4SignerAuth(credentials, region, service)

        client = OpenSearch(
            hosts=[{"host": url, "port": 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            pool_maxsize=20,
        )

        self.client = client

    def create_index(self, index_name, number_of_shards=4):
        index_body = {"settings": {"index": {"number_of_shards": number_of_shards}}}

        return self.client.indices.create(index_name, body=index_body)

    def delete_index(self, index_name):
        return self.client.indices.delete(index=index_name)

    @staticmethod
    def _convert_docs_to_insert_data(index_name, docs):
        data = []
        for doc in docs:
            data.append(
                {
                    "index": {
                        "_index": index_name,
                        "_id": doc.get(
                            "Id", None
                        ),  # test data Reviews.txt has id column title "Id"
                    }
                }
            )
            data.append(doc)
        return "\n".join([json.dumps(doc) for doc in data])

    def upsert_docs(self, index_name, docs):
        data_for_insert = self._convert_docs_to_insert_data(index_name, docs)
        return self.client.bulk(body=data_for_insert)


def split_into_batches(array, max_batch_size):
    batch = []
    for elem in array:
        batch.append(elem)
        if len(batch) == max_batch_size:
            yield batch
            batch = []

    if len(batch) > 0:
        yield batch


def get_lines_count(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return len(list(reader))


if __name__ == "__main__":
    BATCH_SIZE = 50000
    os_url = "search-open-search-hello-world-ptsefi3fh6osw2up7h6mq3ai3a.us-east-1.es.amazonaws.com"
    os_client = OSClient(os_url)
    index_name = "food-reviews-index"
    # dataset is amazon fine food reviews
    # https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews
    filename = "Reviews.csv"

    num_lines = get_lines_count(filename)
    num_batches = math.ceil(num_lines / BATCH_SIZE)

    os_client.delete_index(index_name)
    os_client.create_index(index_name)

    start = perf_counter()
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for docs_batch in tqdm(
            split_into_batches(reader, BATCH_SIZE), total=num_batches
        ):
            response = os_client.upsert_docs(index_name, docs_batch)
            print(f'Took: {response["took"]}ms, Errors: {response["errors"]}')

    end = perf_counter()
    elapsed = end - start
    minutes = int(elapsed / 60)
    seconds = elapsed % 60
    print(f"Elapsed time: {minutes}:{seconds:0.2f}")
