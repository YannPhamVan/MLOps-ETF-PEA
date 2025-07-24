SHELL := /bin/bash

install:
	python -m venv .venv
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && pip install -r requirements.txt; \
	else \
		pip install -r requirements.txt; \
	fi

lint:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && black src tests && flake8 src tests && isort src tests; \
	else \
		black src tests && flake8 src tests && isort src tests; \
	fi

test:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && PYTHONPATH="$(shell pwd)" pytest tests; \
	else \
		PYTHONPATH="$(shell pwd)" pytest tests; \
	fi

format:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && black src tests && isort src tests; \
	else \
		black src tests && isort src tests; \
	fi

ingest:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && PYTHONPATH="$(shell pwd)" python src/data/ingest_etf_data.py; \
	else \
		PYTHONPATH="$(shell pwd)" python src/data/ingest_etf_data.py; \
	fi

feature:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && PYTHONPATH="$(shell pwd)" python src/data/feature_engineering.py; \
	else \
		PYTHONPATH="$(shell pwd)" python src/data/feature_engineering.py; \
	fi

train:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && PYTHONPATH="$(shell pwd)" python src/models/train_model.py; \
	else \
		PYTHONPATH="$(shell pwd)" python src/models/train_model.py; \
	fi

predict:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && PYTHONPATH="$(shell pwd)" python src/models/predict.py; \
	else \
		PYTHONPATH="$(shell pwd)" python src/models/predict.py; \
	fi

build:
	docker build -t etf-mlops-fastapi .

deploy:
	docker run -p 8000:8000 etf-mlops-fastapi

ci-check:
	make lint
	make test

pipeline:
	@if [ -f ".venv/bin/activate" ]; then \
		source .venv/bin/activate && PYTHONPATH="$(shell pwd)" python src/pipeline/prefect_flow.py; \
	else \
		PYTHONPATH="$(shell pwd)" python src/pipeline/prefect_flow.py; \
	fi
