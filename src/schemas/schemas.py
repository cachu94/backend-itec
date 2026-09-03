from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field


class EstadoVehiculo(str, Enum):
    DISPONIBLE = "Disponible"
    EN_SERVICIO = "En Servicio"
    EN_MANTENIMIENTO = "En Mantenimiento"

# Registro Historial de Entrega y Devolución
class Movil(BaseModel):
    id: Annotated[int, Field(gt=0)]
    patente: Annotated[str, Field(min_length=7, max_length=7, examples=["AA123AA"])]
    marca: Annotated[str, Field(min_length=3, examples=["Nissan"])]
    modelo: Annotated[str, Field(min_length=3, examples=["Frontier"])]
    km_inicial: Annotated[int, Field(ge=0, examples=[800])]
    estado: Annotated[EstadoVehiculo, Field(examples=["Disponible"])]

class MovilUpdate(BaseModel):
    patente: Annotated[str, Field(min_length=7, max_length=7, examples=["AA123AA"])]
    marca: Annotated[str, Field(min_length=3, examples=["Nissan"])]
    modelo: Annotated[str, Field(min_length=3, examples=["Frontier"])]
    km_inicial: Annotated[int, Field(ge=0, examples=[800])]
    estado: Annotated[EstadoVehiculo, Field(examples=["Disponible"])]
