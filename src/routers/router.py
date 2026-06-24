from fastapi import APIRouter, HTTPException, Path
from typing import List, Annotated
from datetime import datetime
from src.schemas.models import VehiculoBase, VehiculoResponse, MensajeResponse, VehiculoUpdate

router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehículos GLP"],
)

db_vehiculos = [
    {
        "id": 1,
        "patente": "AA134JP",
        "marca": "Renault",
        "modelo": "Clio",
        "halcon": 5,
        "km_actual": 150100,
        "estado": "Disponible",
        "km_inicio_servicio_o_mantenimiento": 150000,
        "historial": [
            {
                "evento": "Entrega",
                "fecha": "2026-06-22 07:00:00",
                "km_realizados": None,
                "detalles": None
            },
            {
                "evento": "Devolución",
                "fecha": "2026-06-22 15:00:00",
                "km_realizados": 100,
                "detalles": "El vehículo fue devuelto en buen estado."
            }
        ]
    },
    {
        "id": 2,
        "patente": "AG546JL",
        "marca": "Nissan",
        "modelo": "Frontier",
        "halcon": 18,
        "km_actual": 50187,
        "estado": "Disponible",
        "km_inicio_servicio_o_mantenimiento": 50000,
        "historial": [
            {
                "evento": "Entrega",
                "fecha": "2026-06-22 15:00:00",
                "km_realizados": None,
                "detalles": None
            },
            {
                "evento": "Devolución",
                "fecha": "2026-06-22 23:00:00",
                "km_realizados": 187,
                "detalles": "El vehículo fue devuelto en buen estado."
            }
        ]
    },
    {
        "id": 3,
        "patente": "AF913WN",
        "marca": "Peugeot",
        "modelo": "208",
        "halcon": 10,
        "km_actual": 119980,
        "estado": "En Mantenimiento",
        "km_inicio_servicio_o_mantenimiento": 119980,
        "historial": [
            {
                "evento": "En Mantenimiento",
                "fecha": "2026-06-22 15:00:00",
                "km_realizados": None,
                "detalles": "El vehículo fue enviado a mantenimiento por problemas en el motor."
            }
        ]
    }
]  # Simulación de base de datos en memoria

# Obtenemos todos los vehículos
@router.get("/", response_model=List[VehiculoResponse], responses={
    200: {"description": "Lista de vehículos obtenida exitosamente",
        "content": {"application/json": {"example": [
            {
                "id": 1,
                "patente": "AA134JP",
                "marca": "Renault",
                "modelo": "Clio",
                "halcon": 5,
                "km_actual": 150100,
                "estado": "Disponible",
                "km_inicio_servicio_o_mantenimiento": 150000,
                "historial": [
                    {
                        "evento": "Entrega",
                        "fecha": "2026-06-22 07:00:00",
                        "km_realizados": None,
                        "detalles": None
                    },
                    {
                        "evento": "Devolución",
                        "fecha": "2026-06-22 15:00:00",
                        "km_realizados": 100,
                        "detalles": "El vehículo fue devuelto en buen estado."
                    }]
            }]}
        }}
})
async def get_vehiculos():
    return db_vehiculos

# Obtenemos un vehículo por su ID
@router.get("/{id}", response_model=VehiculoResponse, responses={
    200: {"description": "Vehículo encontrado","content": {"application/json": {"example": {
            "id": 1,
            "patente": "AA134JP",
            "marca": "Renault",
            "modelo": "Clio",
            "halcon": 5,
            "km_actual": 150100,
            "estado": "Disponible",
            "km_inicio_servicio_o_mantenimiento": 150000,
            "historial": [
                {
                    "evento": "Entrega",
                    "fecha": "2026-06-22 07:00:00",
                    "km_realizados": None,
                    "detalles": None
                },
                {
                    "evento": "Devolución",
                    "fecha": "2026-06-22 15:00:00",
                    "km_realizados": 100,
                    "detalles": "El vehículo fue devuelto en buen estado."
                }
            ]
        }}}},
    404: {"description": "Vehículo no encontrado","content": {"application/json": {"example": {"detail": "Vehículo no encontrado"}}}}
})
async def get_vehiculo_id(id: Annotated[int, Path(ge=1, description="ID del vehículo")]):
    for vehiculo in db_vehiculos:
        if vehiculo["id"] == id:
            return vehiculo
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")

# Creación o alta de un nuevo vehículo
@router.post("/", status_code=201, response_model=VehiculoResponse, responses={
    201: {"description": "Vehículo creado exitosamente","content": {"application/json": {"example": {
            "id": 4,
            "patente": "AB123CD",
            "marca": "Toyota",
            "modelo": "Corolla",
            "halcon": 20,
            "km_actual": 0,
            "estado": "Disponible",
            "km_inicio_servicio_o_mantenimiento": 0,
            "historial": []
        }}}},
    400: {"description": "Error en la creación del vehículo","content": {"application/json": {"example": {"detail": "Error en la creación del vehículo"}}}}
})
async def create_vehiculo(vehiculo: VehiculoBase):
    nuevo_id = max(v["id"] for v in db_vehiculos) + 1 if db_vehiculos else 1
    nuevo_vehiculo = vehiculo.model_dump()
    nuevo_vehiculo= {"id": nuevo_id, **nuevo_vehiculo}

    if not nuevo_vehiculo["historial"]:
        nuevo_vehiculo["historial"].append({
            "evento": "Alta",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "km_realizados": None,
            "detalles": "Vehículo dado de alta en el sistema."
        })

    db_vehiculos.append(nuevo_vehiculo)
    return nuevo_vehiculo

# Actualización de estado y kilometraje de un vehículo
@router.put("/{id}", response_model=VehiculoResponse, responses={
    200: {"description": "Vehículo actualizado exitosamente","content": {"application/json": {"example": {
            "id": 1,
            "patente": "AA134JP",
            "marca": "Renault",
            "modelo": "Clio",
            "halcon": 5,
            "km_actual": 150200,
            "estado": "En Servicio",
            "km_inicio_servicio_o_mantenimiento": 150100,
            "historial": [
                {
                    "evento": "Entrega",
                    "fecha": "2026-06-22 07:00:00",
                    "km_realizados": None,
                    "detalles": None
                },
                {
                    "evento": "Devolución",
                    "fecha": "2026-06-22 15:00:00",
                    "km_realizados": 100,
                    "detalles": "El vehículo fue devuelto en buen estado."
                },
                {
                    "evento": "Mantenimiento",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "km_realizados": None,
                    "detalles": None
                }
            ]}}}},
    400: {"description": "Error en la actualización del vehículo","content": {"application/json": {"example": {"detail": "Error en la actualización del vehículo"}}}},
    404: {"description": "Vehículo no encontrado","content": {"application/json": {"example": {"detail": "Vehículo no encontrado"}}}},
})
async def update_vehiculo(id: Annotated[int, Path(ge=1, description="ID del vehículo")], datos_vehiculo: VehiculoUpdate):
    for vehiculo in db_vehiculos:
        if vehiculo["id"] == id:
            estado_anterior = vehiculo["estado"]
            estado_nuevo = datos_vehiculo.estado
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            detalle_cargado = datos_vehiculo.detalles if datos_vehiculo.detalles else None

            # CASO 1: ENTREGA (De disponible -> En Servicio)
            if estado_anterior == "Disponible" and estado_nuevo == "En Servicio":
                vehiculo["km_inicio_servicio_o_mantenimiento"] = vehiculo["km_actual"]  # Guardamos el km al inicio del servicio
                vehiculo["historial"].append({
                    "evento": "Entrega",
                    "fecha": fecha_actual,
                    "km_realizados": None,
                    "detalles": detalle_cargado
                })

            # CASO 2: DEVOLUCIÓN (De En Servicio o Mantenimiento-> Disponible)
            elif (estado_anterior=="En Servicio" or estado_anterior=="En Mantenimiento") and estado_nuevo=="Disponible":
                if datos_vehiculo.km_actual < vehiculo["km_inicio_servicio_o_mantenimiento"]:
                    raise HTTPException(status_code=400, detail="El kilometraje actual no puede ser menor al registrado previamente.")
                km_realizados = datos_vehiculo.km_actual - vehiculo["km_inicio_servicio_o_mantenimiento"]
                vehiculo["km_actual"] = datos_vehiculo.km_actual
                vehiculo["historial"].append({
                    "evento": "Devolución",
                    "fecha": fecha_actual,
                    "km_realizados": km_realizados,
                    "detalles": detalle_cargado
                })

            # CASO 3: MANTENIMIENTO (De cualquier estado -> En Mantenimiento)
            elif estado_nuevo == "En Mantenimiento":
                if estado_anterior == "En Servicio":
                    if datos_vehiculo.km_actual < vehiculo["km_inicio_servicio_o_mantenimiento"]:
                        raise HTTPException(status_code=400, detail="El kilometraje actual no puede ser menor al registrado previamente.")
                    km_realizados = datos_vehiculo.km_actual - vehiculo["km_inicio_servicio_o_mantenimiento"]
                    vehiculo["km_actual"] = datos_vehiculo.km_actual
                else:
                    km_realizados = None  # No se registra kilometraje si no estaba en servicio

                vehiculo["km_inicio_servicio_o_mantenimiento"] = datos_vehiculo.km_actual  # Guardamos el km al inicio del mantenimiento
                detalle_cargado = datos_vehiculo.detalles if datos_vehiculo.detalles else None
                vehiculo["historial"].append({
                    "evento": "Mantenimiento",
                    "fecha": fecha_actual,
                    "km_realizados": km_realizados,
                    "detalles": detalle_cargado
                })
            else:
                raise HTTPException(status_code=400, detail=f"Transición de estado no permitida. Estado anterior: {estado_anterior}, Estado nuevo: {estado_nuevo}")

            vehiculo["estado"] = estado_nuevo
            
            return vehiculo
        
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")

# Eliminación de un vehículo de la flota
@router.delete("/{id}", response_model=MensajeResponse, responses={
    200: {"description": "Vehículo eliminado exitosamente","content": {"application/json": {"example": {"detail": "Vehículo eliminado exitosamente"}}}},
    404: {"description": "Vehículo no encontrado","content": {"application/json": {"example": {"detail": "Vehículo no encontrado"}}}},
})
async def delete_vehiculo(id: Annotated[int, Path(ge=1, description="ID del vehículo")]):
    for v in db_vehiculos:
        if v["id"] == id:
            db_vehiculos.remove(v)
            return {"detail": f"Vehículo con patente {v['patente']} eliminado exitosamente."}
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")