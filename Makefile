.PHONY: install lint format test train predict clean

install:
	pipenv install --dev

lint:
	black . --check
	isort . --check
	pylint src/ scripts/ tests/

format:
	black .
	isort .

test:
	pytest tests/

train:
	python notebooks/02_train_model.ipynb

predict:
	python notebooks/03_predict.ipynb

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -r {} +
