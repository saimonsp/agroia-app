# app/models/prediction.py

from pydantic import BaseModel, Field
from typing import Optional

class PredictionData(BaseModel):
    area: float = Field(..., description="Área em hectares")
    crop: str = Field(..., description="Tipo de cultura a ser plantada")
    rainfall: Optional[float] = Field(None, description="Precipitação esperada em mm")
    temperature: Optional[float] = Field(None, description="Temperatura média esperada em °C")
    pest_risk: Optional[float] = Field(None, description="Risco de pragas (0 a 1)")
    disease_risk: Optional[float] = Field(None, description="Risco de doenças (0 a 1)")
    irrigation_needed: Optional[bool] = Field(None, description="Necessidade de irrigação")

    class Config:
        json_schema_extra = {
            "example": {
                "area": 10.0,
                "crop": "Milho",
                "rainfall": 50.0,
                "temperature": 25.0,
                "pest_risk": 0.3,
                "disease_risk": 0.2,
                "irrigation_needed": True
            }
        }
