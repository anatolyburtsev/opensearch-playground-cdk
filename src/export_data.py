import csv
from tqdm import tqdm
import math
from time import perf_counter

from src.OpenSearchClient import OSClient


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
