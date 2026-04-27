import fastapi
from baseDeDatos import SessionLocal

from modelo import Transcripcion

router = fastapi.APIRouter()

@router.get("/historial")
def obtenerHistorial():
    db = SessionLocal()
    try:
        transcripciones = db.query(Transcripcion).all()
        datos = []
        for t in transcripciones:
            datos.append({
                "id": t.id,
                "nombre": t.nombre,
                "texto": t.texto,
                "fecha": t.fecha
            })
        return datos
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()