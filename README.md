# 🚀 MLOps-ETF-PEA - Final Project (MLOps Zoomcamp)

This project applies MLOps best practices for predicting PEA-eligible ETF returns using Prefect, MLflow, Evidently, FastAPI, Docker, Terraform, and LocalStack to achieve full end-to-end automation and reproducibility.

## 🪐 Context
This project automates the full pipeline: ingestion → feature engineering → training → monitoring → prediction, with deployment of a containerized FastAPI API using Docker and cloud simulation via LocalStack.

## 🛠️ Pipeline
- **Ingestion**: retrieving and preparing ETF data.
- **Feature engineering**: creating new explanatory variables.
- **Training**: training regression models tracked with MLflow.
- **Monitoring**: drift monitoring with Evidently.
- **Deployment**: serving a FastAPI API in a Docker container via LocalStack.
- **Orchestration**: Prefect for workflow automation.

## 🚀 Quickstart
1️⃣ Clone this repository and navigate into the project folder:
```bash
git clone https://github.com/YannPhamVan/MLOps-ETF-PEA.git
cd MLOps-ETF-PEA
```

2️⃣ Install dependencies using Pipenv:
```bash
pip install pipenv
pipenv install --dev
```

3️⃣ Run key pipeline steps:
```bash
make ingest        # Ingest ETF data
make feature       # Feature engineering
make train         # Train the model with MLflow tracking
make predict       # Generate batch predictions
```

4️⃣ Deploy the FastAPI service locally:
```bash
make build         # Build the Docker image
make deploy        # Launch the FastAPI container
```

5️⃣ Launch LocalStack for cloud simulation:
```bash
docker-compose up -d
```
This will simulate **S3, Lambda, and API Gateway** locally for testing your pipeline.

6️⃣ Monitor drift using Evidently by running:
```bash
jupyter notebook notebooks/04_monitoring.ipynb
```

7️⃣ Run linting and tests:
```bash
make lint
make test
```

## 📂 Project Structure
- `notebooks/`: EDA, validation, monitoring.
- `data/`: raw data, feature sets, predictions.
- `mlruns/`: MLflow tracking.
- `tests/`: unit and integration tests.
- `src/`: ingestion, feature engineering, model training, prediction scripts.
- `prefect_flows/`: Prefect flows.
- `Dockerfile`, `docker-compose.yml`: deployment and cloud simulation.
- `Makefile`: unified execution.
- `Pipfile`: dependency management.
- `.github/workflows/`: CI/CD pipeline.

## ✅ Best Practices
- Experiment tracking and model registry with MLflow.
- Workflow orchestration with Prefect.
- CI/CD with GitHub Actions.
- Unit and integration testing.
- Pre-commit hooks for linting and formatting (`black`, `flake8`, `isort`).
- Monitoring and drift detection with Evidently.

---

[LinkedIn](https://www.linkedin.com/in/chasseur2valeurs/) | [GitHub](https://github.com/YannPhamVan)