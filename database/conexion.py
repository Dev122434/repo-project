from models.entities import *
from sqlmodel import create_engine, SQLModel

# Conexion a la base de datos
sqlite_file_name = "prueba.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)