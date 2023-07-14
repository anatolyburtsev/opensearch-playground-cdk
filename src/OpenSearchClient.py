import json

import boto3
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection
import concurrent.futures
from itertools import chain


class OSClient:
    def __init__(self, url, index_name, region="us-east-1"):
        service = "es"
        credentials = boto3.Session().get_credentials()
        auth = AWSV4SignerAuth(credentials, region, service)
        self.index_name = index_name

        client = OpenSearch(
            hosts=[{"host": url, "port": 443}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            pool_maxsize=20,
        )

        self.client = client

    def create_index(self, number_of_shards=4):
        index_body = {"settings": {"index": {"number_of_shards": number_of_shards}}}

        return self.client.indices.create(self.index_name, body=index_body)

    def delete_index(self):
        return self.client.indices.delete(index=self.index_name)

    def _convert_docs_to_insert_data(self, docs):
        data = []
        for doc in docs:
            data.append(
                {
                    "index": {
                        "_index": self.index_name,
                        "_id": doc.get(
                            "Id", None
                        ),  # test data Reviews.txt has id column title "Id"
                    }
                }
            )
            data.append(doc)
        return "\n".join([json.dumps(doc) for doc in data])

    def upsert_docs(self, docs):
        data_for_insert = self._convert_docs_to_insert_data(docs)
        return self.client.bulk(body=data_for_insert)

    def search_doc_by_id(self, doc_id):
        response = self.client.search(
            index=self.index_name, body={"query": {"match": {"Id": doc_id}}}
        )
        return response["hits"]["hits"][0]["_source"]

    def search_multiple_docs(self, doc_ids, num_threads):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = executor.map(self.search_doc_by_id, doc_ids)

        return list(results)

    def search_multiple_docs_in_bulk(self, doc_ids):
        data = [
            ({"index": self.index_name}, {"query": {"match": {"Id": doc_id}}})
            for doc_id in doc_ids
        ]
        flat_data = list(chain.from_iterable(data))
        body = "\n".join(json.dumps(query) for query in flat_data)
        response = self.client.msearch(body=body)
        return [resp["hits"]["hits"][0]["_source"] for resp in response["responses"]]
