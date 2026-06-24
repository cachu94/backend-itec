from enum import Enum
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field


class EstadoVehiculo(str, Enum):
    DISPONIBLE = "Disponible"
    EN_SERVICIO = "En Servicio"
    EN_MANTENIMIENTO = "En Mantenimiento"

# Registro Historial de Entrega y Devolución
class RegistroHistorial(BaseModel):
    evento: Annotated[str, Field(description="Tipo de evento: Entrega, Devolución, Mantenimiento")]
    fecha: Annotated[str, Field(description="Fecha y hora del evento")]
    km_realizados: Annotated[Optional[int], Field(ge=0, description="Kilometraje registrado en el evento")] # Se registra en evento de devolución o mantenimiento
    detalles: Annotated[Optional[str], Field(default=None, description="Detalles adicionales del evento")] # Se puede registrar información adicional cuando se devuelve o realiza mantenimiento, como observaciones o comentarios.

# Modelo para la creación y actualización de vehículos
class VehiculoBase(BaseModel):
    patente: Annotated[str, Field(min_length=6, max_length=10, description="Patente del vehículo", examples=["ABC123DEF"])]
    marca: Annotated[str, Field(min_length=3, description="Marca del vehículo", examples=["Volkswagen"])]
    modelo: Annotated[str, Field(min_length=3, description="Modelo del vehículo", examples=["Gol"])]
    halcon: Annotated[int, Field(ge=0, description="Número identificación interna", examples=[20])]
    km_actual: Annotated[int, Field(ge=0, default=0, description="Kilometraje actual del vehículo", examples=[10000])]
    estado: Annotated[EstadoVehiculo, Field(default=EstadoVehiculo.DISPONIBLE, description="Estado: Disponible, En Servicio, En Mantenimiento")]
    km_inicio_servicio_o_mantenimiento: Annotated[int, Field(ge=0, description="Kilometraje al inicio del servicio")] # Se registra en evento de entrega
    historial: Annotated[List[RegistroHistorial], Field(default_factory=list, description="Historial de eventos del vehículo", examples=[{
        "evento": "Entrega",
        "fecha": "2026-06-22 07:00:00",
        "km_realizados": None,
        "detalles": None
    }])]

class VehiculoResponse(VehiculoBase):
    id: Annotated[int, Field(description="ID del vehículo")]

class MensajeResponse(BaseModel):
    detail: Annotated[str, Field(description="Mensaje de resultado de la operación")]

class VehiculoUpdate(BaseModel):
    estado: Annotated[EstadoVehiculo, Field(description="Nuevo estado del vehículo: Disponible, En Servicio, En Mantenimiento")]
    km_actual: Annotated[int, Field(ge=0, description="Kilometraje actual del vehículo, requerido si pasa de Servicio a Disponible, de Mantenimiento a Disponible o de Servicio a Mantenimiento")]
    detalles: Annotated[Optional[str], Field(default=None, description="Detalles adicionales del evento, como observaciones o comentarios")]