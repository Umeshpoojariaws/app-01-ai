import mlflow
from fastapi import FastAPI, Response
from pydantic import BaseModel
import pandas as pd
import os
from mlflow.tracking import MlflowClient

# Set the MLFLOW_TRACKING_URI environment variable
os.environ['MLFLOW_TRACKING_URI'] = 'http://mlflow:5000'

app = FastAPI()
model = None

@app.on_event("startup")
def load_model():
    global model
    model_name = "weather-forecaster"
    client = MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["None"])[0].version
    
    # Load the model after the server starts
    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{latest_version}")

class PredictionPayload(BaseModel):
    today_temp: float
    humidity: float
    wind_speed: float

@app.get("/health")
def health_check(response: Response):
    if model is None:
        response.status_code = 503
        return {"status": "model_not_ready"}
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: PredictionPayload):
    if model is None:
        return {"error": "Model is not loaded yet"}, 503
    data = pd.DataFrame([payload.dict()])
    prediction = model.predict(data)
    return {"prediction": prediction.tolist()}