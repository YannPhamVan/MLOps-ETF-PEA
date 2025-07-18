install:
	pipenv install --dev

lint:
	pipenv run black src tests
	pipenv run flake8 src tests
	pipenv run isort src tests

test:
	pipenv run pytest tests

format:
	pipenv run black src tests
	pipenv run isort src tests

ingest:
	pipenv run python src/data/ingest_etf_data.py

feature:
	pipenv run python src/data/feature_engineering.py

train:
	pipenv run python src/models/train_model.py

predict:
	pipenv run python src/models/predict.py

build:
	docker build -t etf-mlops-fastapi .

deploy:
	docker run -p 8000:8000 etf-mlops-fastapi

ci-check:
	make lint
	make test