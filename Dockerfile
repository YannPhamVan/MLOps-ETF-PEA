FROM python:3.11-slim

WORKDIR /app

COPY Pipfile* ./
RUN pip install pipenv && pipenv install --system --deploy

COPY . .

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]