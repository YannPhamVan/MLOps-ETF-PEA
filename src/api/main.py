import pickle

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="ETF Return Prediction API", description="MLOps Zoomcamp Final Project"
)

# Load model once at startup
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)


class ETFInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    # Add all required features here


@app.get("/")
def read_root():
    return {"message": "Welcome to the ETF Return Prediction API"}


@app.post("/predict")
def predict_etf(input_data: ETFInput):
    try:
        df = pd.DataFrame([input_data.dict()])
        prediction = model.predict(df)[0]
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
