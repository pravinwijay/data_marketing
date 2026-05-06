import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from schemas import MarketingData, PredictionResponse

app = FastAPI(
    title="API ROI",
    description="API permettant de prédire les ventes basées sur les budgets publicitaires.",
)

try:
    model = joblib.load('../models/gradient_boosting_pipeline.pkl')
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict_sales(data: MarketingData):
    try:
        data_dict = {
            "TV": data.TV,
            "Radio": data.Radio,
            "Social Media": data.Social_Media,
            "Influencer": data.Influencer
        }
        
        df_input = pd.DataFrame([data_dict])
        prediction = model.predict(df_input)
        
        return {"predicted_sales_millions": round(float(prediction[0]), 2)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))