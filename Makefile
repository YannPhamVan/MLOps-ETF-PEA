install:
	python -m venv .venv
	source .venv/Scripts/activate && pip install -r requirements.txt

lint:
	source .venv/Scripts/activate && black src tests
	source .venv/Scripts/activate && flake8 src tests
	source .venv/Scripts/activate && isort src tests

test:
	PYTHONPATH=. source .venv/Scripts/activate && pytest tests

format:
	source .venv/Scripts/activate && black src tests
	source .venv/Scripts/activate && isort src tests

ingest:
	PYTHONPATH=. source .venv/Scripts/activate && python src/data/ingest_etf_data.py

feature:
	PYTHONPATH=. source .venv/Scripts/activate && python src/data/feature_engineering.py

train:
	PYTHONPATH=. source .venv/Scripts/activate && python src/models/train_model.py

predict:
	PYTHONPATH=. source .venv/Scripts/activate && python src/models/predict.py

build:
	docker build -t etf-mlops-fastapi .

deploy:
	docker run -p 8000:8000 etf-mlops-fastapi

ci-check:
	make lint
	make test
