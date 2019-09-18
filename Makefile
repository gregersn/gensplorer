.PHONY: test
test:
	python3 -m pytest

.PHONY: coverage
coverage:
	python3 -m pytest --cov-report term-missing --cov=gensplorer