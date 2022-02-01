.PHONY: help build shell test format clean

.DEFAULT: help

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

test: ## Run flake8 syntax and codestyle check, then run tests with pytest
	flake8 src
	flake8 tests
	pytest
	make clean

format: ## Format with black, then run flake8 syntax and codestyle check
	black src tests
	flake8 src tests

clean: ## Delete /.pytest_cache and tests/__pycache__
	rm -rf .pytest_cache **/__pycache__

init-githook: ## Remove any symlink from .git/hooks, then symlink the /.githooks folder into .git/hooks (this way we can share git-hooks on github)
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;
