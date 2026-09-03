from src.database import Base
from sqlalchemy import Column, Integer, String

class Movil(Base):
    __tablename__ = "moviles"

    id = Column(Integer, primary_key=True, index=True)
    patente = Column(String)
    marca = Column(String)
    modelo = Column(String)
    km_inicial = Column(Integer)
    estado = Column(String)