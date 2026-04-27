from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import whisper
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

from baseDeDatos import SessionLocal
from modelo import Transcripcion
from verificarArchivo import verificarArchivo
from TransPorNombre import router as buscarPorNombre
from obtenerDatosDB import router as obtenerHistorial

app = FastAPI()
app.add_middleware(
    CORSMiddleware,

    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(buscarPorNombre)
app.include_router(obtenerHistorial)

#Cargamos el modelo de Whisper
modelo = whisper.load_model("base")

@app.post("/transcribe")
async def transcribeAudio(nombre : str = Form(...), archivo: UploadFile = File(...)):
    try:
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
        print("Archivo guardado")    
        #Transcribir el audio
        resultado = modelo.transcribe(f"Archivo/{temporalFile}")
        print("Transcripcion hecha")
        #Obtener el texto transcrito
        texto = resultado["text"]
        #Guardar en la base de datos
        guardarEnLaBaseDeDatos(nombre, texto)

        try:
            os.remove(f"Archivo/{temporalFile}")
        except Exception as e:
            print("Error eliminando archivo:", e)

        return{
            "mensaje": "ok",
            "nombre": nombre,
            "transcripcion" : texto
        }
    except Exception as e:
        return{
            "Error" : str(e)
        }

def guardarEnLaBaseDeDatos(nombre, texto):
    db = SessionLocal()    
    try:
        nuevaTranscripcion = Transcripcion(
            nombre=nombre.lower(),
            texto=texto
        )

        db.add(nuevaTranscripcion)
        db.commit()

    finally:
        db.close()