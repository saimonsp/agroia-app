from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.prediction import predict

app = FastAPI()

@app.post("/predict/")
async def predict_endpoint(file: UploadFile = File(...)):
    # Salvar o arquivo recebido temporariamente
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Chamar a função de predição
    try:
        predictions, img_str = predict(file_location)
        
        # Retornar a imagem gerada em base64
        return JSONResponse(content={
            "predictions": predictions,
            "image": img_str,
            "image_format": "png"  # Especifica o formato da imagem
        })
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
