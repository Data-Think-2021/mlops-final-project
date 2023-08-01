quality_checks:
	black .
	isort .
	pylint --recuisive=y .

test:
	pytest tests/

build: quality_checks test
	docker build -t mlops-zoomcamp-bbc-news-clustering:v1 .

publish: build

setup:
	pipenv install --dev
	pre-commit install