from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from baseDeDatos import Base

class Transcripcion(Base):
    __tablename__ = "Transcripciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    texto = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)
