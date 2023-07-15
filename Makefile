.PHONY: install lint-fix lint deploy build-docker
install:
	poetry install && poetry shell
lint-fix:
	black .
lint:
	black --check --quiet . && ruff .
pre-commit:
	pre-commit run --all-files
deploy:
	cdk deploy
