SHELL := /bin/bash

ifeq ($(OS),Windows_NT)
	ACTIVATE = .venv/Scripts/activate
else
	ACTIVATE = source .venv/bin/activate
endif

install:
	python -m venv .venv
	$(ACTIVATE) && pip install -r requirements.txt

lint:
	$(ACTIVATE) && black src tests
	$(ACTIVATE) && flake8 src tests
	$(ACTIVATE) && isort src tests

test:
	PYTHONPATH=$(pwd) .venv/Scripts/python.exe -m pytest tests
	

format:
	$(ACTIVATE) && black src tests
	$(ACTIVATE) && isort src tests

ingest:
	PYTHONPATH="$(shell pwd)" $(ACTIVATE) && python src/data/ingest_etf_data.py

feature:
	PYTHONPATH="$(shell pwd)" $(ACTIVATE) && python src/data/feature_engineering.py

train:
	PYTHONPATH="$(shell pwd)" $(ACTIVATE) && python src/models/train_model.py

predict:
	PYTHONPATH="$(shell pwd)" $(ACTIVATE) && python src/models/predict.py

build:
	docker build -t etf-mlops-fastapi .

deploy:
	docker run -p 8000:8000 etf-mlops-fastapi

ci-check:
	make lint
	make test
