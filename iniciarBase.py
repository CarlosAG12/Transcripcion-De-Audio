from baseDeDatos import engine
from modelo import Base
Base.metadata.create_all(bind=engine)