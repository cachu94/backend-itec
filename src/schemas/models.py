from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

# Registro Historial de Entrega y Devolución
class RegistroHistorial(BaseModel):
    evento: Annotated[str, Field(description="Tipo de evento: Entrega, Devolución, Mantenimiento")]
    fecha: Annotated[str, Field(description="Fecha y hora del evento")]
    km_realizados: Annotated[Optional[int], Field(ge=0, description="Kilometraje registrado en el evento")] # Se registra en evento de devolución o mantenimiento
    detalles: Annotated[Optional[str], Field(default=None, description="Detalles adicionales del evento")] # Se puede registrar información adicional cuando se devuelve o realiza mantenimiento, como observaciones o comentarios.

# Modelo para la creación y actualización de vehículos
class VehiculoBase(BaseModel):
    patente: Annotated[str, Field(min_length=6, max_length=10, description="Patente del vehículo")]
    marca: Annotated[str, Field(min_length=3, description="Marca del vehículo")]
    modelo: Annotated[str, Field(min_length=3, description="Modelo del vehículo")]
    halcon: Annotated[int, Field(ge=0, description="Número identificación interna")]
    km_actual: Annotated[int, Field(ge=0, default=0, description="Kilometraje actual del vehículo")]
    estado: Annotated[str, Field(default="Disponible", description="Estado: Disponible, En Servicio, En Mantenimiento")]
    km_inicio_servicio_o_mantenimiento: Annotated[int, Field(ge=0, description="Kilometraje al inicio del servicio")] # Se registra en evento de entrega
    historial: Annotated[List[RegistroHistorial], Field(default=[], description="Historial de eventos del vehículo")]


class VehiculoResponse(VehiculoBase):
    id: Annotated[int, Field(description="ID del vehículo")]