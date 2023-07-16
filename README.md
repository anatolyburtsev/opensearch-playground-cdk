# Repository Description
This repository contains a comparative benchmark analysis between multithreaded search queries and batch searches on an OpenSearch cluster. As our experiments show, batch searches are considerably more efficient. We recommend implementing them for faster results.

### The Experiment
For our OpenSearch cluster, we used a substantial dataset detailed below. Our experiment involved generating a list of unique random ids and fetching corresponding documents using both [Multisearch](https://opensearch.org/docs/latest/api-reference/multi-search/) and regular [Search](https://opensearch.org/docs/latest/api-reference/search/) operations, carried out in multiple threads. We conducted our tests using 1, 3, 6, 12, 25, 50, and 100 threads, ensuring the same list of randomly generated document ids was used across all tests.

The number of documents searched varied, including: 100, 1000, 3000, 5000, 10000. In each instance, MultiSearch outperformed the regular Search. Furthermore, we noticed a trend: the larger the number of documents, the greater the performance gap favoring MultiSearch.

Please note: We used Query by id instead of a Get operation intentionally. This was to mirror a realistic use-case scenario, although a Get operation would typically be faster.

![diagram.png](assets%2Fdiagram.png)

### Results

| Number of Docs to Search | Multisearch Time (secs) | 100 Threads Time (secs) | 50 Threads Time (secs) | 25 Threads Time (secs) | 12 Threads Time (secs) | 6 Threads Time (secs) | 3 Threads Time (secs) | 1 Thread Time (secs) |
|--------------------------|-------------------------|-------------------------|------------------------|------------------------|------------------------|-----------------------|-----------------------|---------------------|
| 100                      | 1.18                    | 1.73                    | 0.71                   | 0.83                   | 1.03                   | 1.77                  | 3.56                  | 10.04               |
| 1000                     | 3.41                    | 3.49                    | 5.03                   | 6.59                   | 14.87                  | 18.25                 | 36.99                 | 105.29              |
| 3000                     | 9.37                    | 14.06                   | 15.24                  | 19.37                  | 30.3                   | 57.78                 | 109.32                | 315.59              |
| 5000                     | 6.17                    | 22.03                   | 22.62                  | 28.31                  | 50.56                  | 89.42                 | 170.82                | 506.36              |
| 10000                    | 15.59                   | 40.36                   | 57.31                  | 64.63                  | 105.58                 | 181.62                | 323.91                | 1010.07             |

The benchmarking experiment shows a clear advantage for Multisearch over single-threaded and multi-threaded searches in OpenSearch clusters, particularly as the document count increases. Even against 100 threads, Multisearch performed significantly faster across all tests, ranging from 100 to 10,000 documents. These findings highlight Multisearch as a superior search method, providing considerable efficiency benefits when handling large datasets.

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
