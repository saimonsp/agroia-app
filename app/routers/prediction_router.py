# app/routers/predictions.py

from fastapi import APIRouter, HTTPException
from app.prediction import predict

router = APIRouter()

@router.post("/predict/")
async def make_prediction(coordinates: dict):
    try:
        # Extrair as coordenadas do corpo da requisição
        lat = coordinates.get("latitude")
        lon = coordinates.get("longitude")
        if lat is None or lon is None:
            raise HTTPException(status_code=400, detail="Coordenadas inválidas")

        # Chamar a função de predição
        result = predict((lat, lon))
        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
