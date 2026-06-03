from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.agente_meli import ejecutar_agente


class MensajeRequest(BaseModel):
    mensaje:str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analizar")
def analizar_mensaje(request: MensajeRequest):
    try:
        msj = ejecutar_agente(request.mensaje)
        return msj
    except ValueError:
        raise HTTPException(status_code=500, detail="Error al procesar la respuesta de Claude")
