from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import whisper
import shutil
import os

from baseDeDatos import SessionLocal
from modelo import Transcripcion
from verificarArchivo import verificarArchivo
from TransPorNombre import router as buscarPorNombre
from obtenerDatosDB import router as obtenerHistorial

app = FastAPI()
app.include_router(buscarPorNombre)
app.include_router(obtenerHistorial)

#Cargamos el modelo de Whisper
modelo = whisper.load_model("base")

@app.post("/transcribe")
async def transcribeAudio(nombre : str = Form(...), archivo: UploadFile = File(...)):

    #Verificar el archivo
    esValido, mensaje = verificarArchivo(nombre, archivo)
    if not esValido:
        return {"error": mensaje}
    
    #Guardar archivo temporalmente
    temporalFile = f"temp_{archivo.filename}"

    #Verificar que la carpeta temporal exista, si no, crearla
    if not os.path.exists("Archivo"):
        os.makedirs("Archivo")

    #Escribir el archivo temporalmente
    with open(f"Archivo/{temporalFile}", "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
    
    #Transcribir el audio
    resultado = modelo.transcribe(f"Archivo/{temporalFile}")
    #Obtener el texto transcrito
    texto = resultado["text"]

    #Guardar en la base de datos
    guardarEnLaBaseDeDatos(nombre, texto)

    os.remove(f"Archivo/{temporalFile}")
    return{
        "mensaje": mensaje,
        "nombre": nombre,
        "transcripcion": texto
    }

def guardarEnLaBaseDeDatos(nombre, texto):
    db = SessionLocal()    
    #Guardar en la base de datos
    nuevaTranscripcion = Transcripcion(nombre=nombre.lower(), texto=texto)
    #Se agrega la transcripción a la sesión de la base de datos
    db.add(nuevaTranscripcion)
    #Se guarda la transcripción en la base de datos
    db.commit()

