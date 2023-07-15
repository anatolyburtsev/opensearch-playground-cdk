# Description
Repository is created to benchmark multithread search queries vs batch one for OpenSearch cluster.

**Spoiler**: Batch is much-much faster, use it.

### Experiment description
OpenSearch cluster has one index with big dataset described below.
Generate list of unique random ids and get corresponding documents using [Multisearch](https://opensearch.org/docs/latest/api-reference/multi-search/)
and regular [Search](https://opensearch.org/docs/latest/api-reference/search/) in multiple threads. Number of threads I tried are:
1, 3, 6, 12, 25, 50, 100. Same list of randomly generated document ids was used.

I run several experiments for different numbers of documents to find: 100, 1000, 3000, 5000, 10000. MultiSearch was always faster.
The bigger was the number of experiments, the bigger gain MultiSearch has.



Note: Get operation would be faster than Query by id. Query is used intentionally to close recreate real use-case.


### Infrastructure description
```
Cloud: AWS
OpenSearch v2.5,
Instance: r5.large.search
Number of nodes: 1
EBS: gp2, 20Gb
```

### Dataset description
Amazon Fine Food Reviews from Kaggle. [Link](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)

568,454 reviews, ~300Mb in csv

[Sample review](./assets/doc_sample.json)

Uploaded them to OpenSearch using [./src/export_data.py](./src/export_data.py) script

![os-searchable-doc-screenshot.png](assets%2Fos-searchable-doc-screenshot.png)

## Local development
### Prerequisites
- [python 3.11](https://www.python.org/downloads/)
- [poetry](https://python-poetry.org/docs/) - modern python dependencies manager.
- [Pycharm](https://www.jetbrains.com/help/pycharm/installation-guide.html) Jetbrain’s IDE for python
- [BlackConnect plugin](https://plugins.jetbrains.com/plugin/14321-blackconnect) - plugin for Pycharm to auto-reformat code
- [Ruff plugin](https://plugins.jetbrains.com/plugin/20574-ruff) - plugin for Pycharm to help with code quality

### Install dependencies
```shell
poetry install
```
### Activate environment (Optional)
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

## Deploy to AWS account
0. Prepare AWS credentials
1. Deploy. Run from root folder
 ```
 cdk deploy
 ```
### Run pre-commit hooks manually
```shell
pre-commit run --all-files
```
