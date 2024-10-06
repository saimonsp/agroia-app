from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from .. import models, crud, prediction
from app.db import get_db  # Use a importação absoluta


router = APIRouter()

@router.post("/predict/")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Ler o arquivo HDF5
    contents = await file.read()
    
    # Salvar o arquivo temporariamente
    file_path = "temp_file.h5"
    with open(file_path, "wb") as temp_file:
        temp_file.write(contents)

    # Chamar a função de predição
    predictions, heatmap = prediction.predict(file_path)

    # Gravar os dados no banco de dados
    new_prediction = models.Prediction(
        predictions=predictions,
        heatmap_image=heatmap
    )
    crud.create_prediction(db=db, prediction=new_prediction)

    return {"predictions": predictions, "heatmap": heatmap}
