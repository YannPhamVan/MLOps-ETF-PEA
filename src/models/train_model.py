#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 02_train_model.ipynb


import mlflow
# 📌 1️⃣ Imports et config
import pandas as pd
from lightgbm import LGBMRegressor, early_stopping
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

# In[2]:


# 📌 2️⃣ Paramètres
EXPERIMENT_NAME = "ETF_PEA_MLOpsZoomcamp"
mlflow.set_tracking_uri("file:///G:/Mon Drive/DataTalksClub/MLOps-ETF-PEA/mlruns")
mlflow.set_experiment(EXPERIMENT_NAME)


# In[3]:


# 📌 3️⃣ Chargement des données
df = pd.read_parquet("../data/df_all.parquet")
print(f"✅ Data shape: {df.shape}")

feature_cols = [col for col in df.columns if col not in ["target", "ticker"]]
X = df[feature_cols]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# In[4]:


# 📌 4️⃣ Gestion du Registered Model
client = MlflowClient()
try:
    client.create_registered_model(EXPERIMENT_NAME)
    print(f"✅ Registered model '{EXPERIMENT_NAME}' created.")
except MlflowException as e:
    if "already exists" in str(e):
        print(
            f"✅ Registered model '{EXPERIMENT_NAME}' \
               already exists, continuing."
        )
    else:
        raise e


# In[5]:


# 📌 5️⃣ Tracking et training
params = {
    "learning_rate": 0.01,
    "num_leaves": 31,
    "max_depth": -1,
    "random_state": 42,
}

with mlflow.start_run() as run:
    mlflow.log_params(params)

    model = LGBMRegressor(**params, n_estimators=100)

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        callbacks=[early_stopping(stopping_rounds=10)],
    )

    y_pred = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    print(f"✅ Training completed with RMSE: {rmse:.5f}, R²: {r2:.5f}")

    # Log du modèle
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=EXPERIMENT_NAME,
        input_example=X_test.iloc[:5],
    )

    print(f"✅ Model logged and registered under '{EXPERIMENT_NAME}'")
