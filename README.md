# Repository Description
This repository contains a comparative benchmark analysis between multithreaded search queries and batch searches on an OpenSearch cluster. As our experiments show, batch searches are considerably more efficient. We recommend implementing them for faster results.

### The Experiment
For our OpenSearch cluster, we used a substantial dataset detailed below. Our experiment involved generating a list of unique random ids and fetching corresponding documents using both [Multisearch](https://opensearch.org/docs/latest/api-reference/multi-search/) and regular [Search](https://opensearch.org/docs/latest/api-reference/search/) operations, carried out in multiple threads. We conducted our tests using 1, 3, 6, 12, 25, 50, and 100 threads, ensuring the same list of randomly generated document ids was used across all tests.

The number of documents searched varied, including: 100, 1000, 3000, 5000, 10000. In each instance, MultiSearch outperformed the regular Search. Furthermore, we noticed a trend: the larger the number of documents, the greater the performance gap favoring MultiSearch.

Please note: We used Query by id instead of a Get operation intentionally. This was to mirror a realistic use-case scenario, although a Get operation would typically be faster.

### Infrastructure
The OpenSearch cluster was hosted on AWS using the following specifications:
```
- OpenSearch v2.5
- Instance: r5.large.search
- Number of nodes: 1
- EBS: gp2, 20Gb
```

### Dataset
Our dataset was the 'Amazon Fine Food Reviews' from Kaggle [Link](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews). This dataset consists of 568,454 reviews, approximately 300Mb in a CSV file.
We uploaded the reviews to OpenSearch using the [./src/export_data.py](./src/export_data.py) script. A sample review can be found [here](./assets/doc_sample.json).

## Local development
### Prerequisites
- [python 3.11](https://www.python.org/downloads/)
- [poetry](https://python-poetry.org/docs/) (python dependencies manager).
- [Pycharm](https://www.jetbrains.com/help/pycharm/installation-guide.html) (Python IDE)
- [BlackConnect plugin](https://plugins.jetbrains.com/plugin/14321-blackconnect) (for auto-reformatting code in PyCharm)
- [Ruff plugin](https://plugins.jetbrains.com/plugin/20574-ruff) (for code quality assistance in PyCharm)

## Setup
### Install dependencies
```shell
poetry install
```
### (Optional) Activate environment
```shell
poetry shell
```
### Install pre-commit hooks
```shell
poetry run pre-commit install
```
### Add new python dependency
```shell
poetry add new-package-name
```

## Deployment to AWS account
0. Prepare AWS credentials
1. To deploy from root folder, use:
 ```
 cdk deploy
 ```
### Run pre-commit hooks manually
To execute pre-commit hooks manually:
```shell
pre-commit run --all-files
```
