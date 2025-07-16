#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 📌 03_predict.ipynb - Predict ETF forward returns with registered MLflow model

from pathlib import Path

import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from sklearn.metrics import r2_score, root_mean_squared_error

# In[2]:


# 🚩 Config
EXPERIMENT_NAME = "ETF_PEA_MLOpsZoomcamp"
TRACKING_URI = "file:///G:/Mon Drive/DataTalksClub/MLOps-ETF-PEA/mlruns"

DATA_PATH = Path("../data/df_all.parquet")
PREDICTIONS_DIR = Path("../data/predictions")
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)


# In[3]:


# 🚩 Init MLflow
mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient()


# In[4]:


# ✅ Load latest model version from Registry
model_name = EXPERIMENT_NAME
latest_versions = client.get_latest_versions(model_name, stages=["None"])
model_uri = f"models:/{model_name}/{latest_versions[0].version}"

model = mlflow.pyfunc.load_model(model_uri)
print(f"✅ Model v{latest_versions[0].version} loaded from MLflow Registry.")


# In[5]:


# ✅ Load data
df_all = pd.read_parquet(DATA_PATH)
print(f"✅ Data shape: {df_all.shape}")


# In[6]:


# ✅ Predict
feature_cols = [col for col in df_all.columns if col not in ["target", "ticker"]]
X = df_all[feature_cols]
y_true = df_all["target"]

y_pred = model.predict(X)


# In[7]:


# ✅ Save predictions
df_all["prediction"] = y_pred
pred_file = PREDICTIONS_DIR / "predictions.parquet"
df_all.to_parquet(pred_file, index=False)
print(f"✅ Predictions saved to {pred_file}")


# In[8]:


# ✅ Quick evaluation
rmse = root_mean_squared_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
print(f"✅ Evaluation on full dataset -> RMSE: {rmse:.5f}, R²: {r2:.5f}")


# In[9]:


# ✅ Display sample
df_all[["target", "prediction"]].head()
