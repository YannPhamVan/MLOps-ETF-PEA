SHELL := /bin/bash
PYTHON := PYTHONPATH=. python

install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

lint:
	black src tests
	flake8 src tests
	isort src tests

test:
	$(PYTHON) -m pytest tests

format:
	black src tests
	isort src tests

create-bucket:
	aws --endpoint-url=http://localhost:4566 s3 mb s3://mlops-etf-pea-bucket || true

ingest: create-bucket
	$(PYTHON) src/data/ingest_etf_data.py

feature:
	$(PYTHON) src/data/feature_engineering.py

train:
	MLFLOW_TRACKING_URI=mlruns $(PYTHON) src/models/train_model.py

predict:
	$(PYTHON) src/models/predict.py

build:
	docker build -t etf-mlops-fastapi .

deploy:
	docker run -p 8000:8000 etf-mlops-fastapi

ci-check: lint test

pipeline: create-bucket
	MLFLOW_TRACKING_URI=mlruns \
	PYTHONPATH="$(shell pwd)" \
	python src/pipeline/prefect_flow.py
