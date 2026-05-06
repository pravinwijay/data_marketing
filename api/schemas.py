from pydantic import BaseModel, Field

class MarketingData(BaseModel):
    TV: float = Field(..., description="Budget TV en millions", ge=0)
    Radio: float = Field(..., description="Budget Radio en millions", ge=0)
    Social_Media: float = Field(..., description="Budget Social Media en millions", ge=0)
    Influencer: str = Field(..., description="Type d'influenceur (Mega, Macro, Micro, Nano)")

class PredictionResponse(BaseModel):
    predicted_sales_millions: float