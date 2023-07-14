import json

import boto3
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection


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
