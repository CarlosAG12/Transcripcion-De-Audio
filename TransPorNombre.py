import fastapi 
from baseDeDatos import SessionLocal
import modelo as modelo
router = fastapi.APIRouter()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/nombres")
def buscarPorNombre(nombre: str, db = fastapi.Depends(getDb)):
    try:
        transcripcion =  db.query(modelo.Transcripcion).filter(modelo.Transcripcion.nombre == nombre).all()
        if transcripcion:
            return {
                "nombre": transcripcion[0].nombre,
                "texto": transcripcion[0].texto,
                "fecha": transcripcion[0].fecha
            }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()