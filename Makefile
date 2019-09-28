.PHONY: test
test:
	pytest

.PHONY: coverage
coverage:
	pytest --cov-report term-missing --cov=gensplorer