from fastapi import FastAPI, Body, HTTPException, Path, Query
from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum


app = FastAPI()

app.title = "Giacri Facundo - Práctico 1: Crud en memoria con FastAPI"
app.summary =  "Consumo de Presupuesto"


db_agentes = [
    {"id": 1, "apellido": "Arguello" ,"nombre": "Abigail",  "cargo": "jefe de turno", "pres_asig": 36, "pres_cons": 18},
    {"id": 2, "apellido": "Ricca" ,"nombre": "David",  "cargo": "1° ayudante", "pres_asig": 36, "pres_cons": 17},
    {"id": 3, "apellido": "Rodriguez" ,"nombre": "Gimena",  "cargo": "2° ayudante", "pres_asig": 36, "pres_cons": 19.75},
    {"id": 4, "apellido": "Depetris" ,"nombre": "Agustin",  "cargo": "agente", "pres_asig": 24, "pres_cons": 6},
    {"id": 5, "apellido": "Diez" ,"nombre": "Mario",  "cargo": "director", "pres_asig": 42, "pres_cons": 21},
]

db_sueldos_base = [
    {"id": 1, "cargo": "director", "sueldo_base": 1000}
]
db_precios_especiales = [
    {"id": 1, "descripcion": "Precio por hora adicional", "precio": 10},
    {"id": 2, "descripcion": "Precio por turno fin de semana o feriado", "precio": 50}
]

class CargosEnum(str, Enum):
    director = "director"
    subdirector = "subdirector"
    administrador = "admnistrador"
    secretaria = "secretaria"
    logistico = "logistico"
    capacitadora = "capacitadora"
    jefe_de_turno = "jefe de turno"
    primer_ayudante = "1° ayudante"
    segundo_ayudante = "2° ayudante"
    agente = "agente"

class PreciosEspecialesEnum(str, Enum):
    precio_hora_adicional = "Precio por hora adicional"
    precio_turno_finde = "Precio por turno fin de semana o feriado"

class AgenteModel(BaseModel):
    id: Annotated[int, Field(gt=0, examples=[2])]
    apellido: Annotated[str, Field(min_length=3, max_length=20, examples=["Lay"])]
    nombre: Annotated[str, Field(min_length=3, max_length=20, examples=["Ana"])]
    cargo: CargosEnum
    pres_asig: Annotated[int, Field(gt=0, examples=[36], default=36)]
    pres_cons: Annotated[float, Field(default=0)]

class SueldosBase(BaseModel):
    id: Annotated[int, Field(gt=0, examples=[2])]
    cargo: CargosEnum
    sueldo_base: Annotated[int, Field(gt=0, examples=[1000])]

class PrecioEspecial(BaseModel):
    id: Annotated[int, Field(gt=0, examples=[2])]
    descripcion: Annotated[str, Field(min_length=3, max_length=50, examples=["Precio por hora adicional"])]
    precio: Annotated[int, Field(gt=0, examples=[500])]

class SueldoBaseUpdate(BaseModel):
    cargo: CargosEnum
    sueldo_base: Annotated[int, Field(gt=0, examples=[1000])]

class PrecioEspecialUpdate(BaseModel):
    descripcion: Annotated[str, Field(min_length=3, max_length=50, examples=["Precio por hora adicional"])]
    precio: Annotated[int, Field(gt=0, examples=[500])]

class PresupuestoSobrante(BaseModel):
    agente: Annotated[str, Field(min_length=3, max_length=50, examples=["Ana Lay"])]
    pres_sobrante: Annotated[float, Field(gt=0, examples=[18])]

class CalcularSueldo(BaseModel):
    Agente: str
    Cargo: CargosEnum
    Sueldo_Base: Annotated[float, Field(gt=0, examples=[1000])]
    tfsyf: Annotated[float, Field(gt=0, examples=[1000])]
    Hs_Adicionales: Annotated[float, Field(gt=0, examples=[1000])]
    Total: Annotated[float, Field(gt=0, examples=[1000])]

# --------------- SUELDOS BASE ---------------
# CREAR SUELDO BASE
@app.post("/cargar-sueldo", tags=["SUELDOS"], response_model=list[SueldosBase], responses={
    409:{"description":"El id ya existe",
        "content":{
            "application/json": {
                "example": {
                    "detail": "El id ya existe"
                }
            }
        }},
    422:{"description":"Error de validación",
        "content":{
            "application/json": {
                "example": {
                    "detail": "El cargo no es válido"
                }
            }
        }}
})
def crear_sueldo_base(sueldo_base: SueldosBase):
    for sueldo in db_sueldos_base:
        if sueldo["id"] == sueldo_base.id:
            raise HTTPException(409, detail="El id ya existe")
        
    db_sueldos_base.append(sueldo_base.model_dump())
    return db_sueldos_base

@app.post("/cargar-precio-hs-extras", tags=["SUELDOS"], response_model=PrecioEspecial, responses={
    409:{"description":"El id ya existe",
        "content":{
            "application/json": {
                "example": {
                    "detail": "El id ya existe"
                }
            }
        }}})
def cargar_precio_extra(precio_especial: PrecioEspecial):
    for p in db_precios_especiales:
        if p["id"] == precio_especial.id:
            raise HTTPException(409, detail="El id ya existe")
    db_precios_especiales.append(precio_especial.model_dump())
    return precio_especial

# LISTAR SUELDOS BASE
@app.get("/sueldos_base", tags=["SUELDOS"], responses={
    404:{"description":"No hay sueldos cargados",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Sin datos"
                }
            }
        }}
})
def listar_sueldos_base() -> list[SueldosBase]:
    if len(db_sueldos_base) < 1:
        raise HTTPException(404, detail="No hay sueldos cargados")
    listado = []
    for sb in db_sueldos_base:
        listado.append(sb)
    return listado

# LISTAR PRECIOS ESPECIALES
@app.get("/precios-especiales", tags=["SUELDOS"], responses={
    404:{"description":"No hay precios especiales cargados",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Sin datos"
                }
            }
        }}
})
def listar_precios_especiales() -> list[PrecioEspecial]:
    if len(db_precios_especiales) < 1:
        raise HTTPException(404, detail="No hay precios especiales cargados")
    listado = []
    for p in db_precios_especiales:
        listado.append(p)
    return listado

# OBTENER SUELDO BASE POR ID
@app.get("/sueldo-base/{id}", response_model=SueldosBase, tags=["SUELDOS"], responses={
    404:{"description":"Sueldo base no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Sueldo base no encontrado"
                }
            }
        }}
})
def obtener_sueldo_base_por_id(id: Annotated[int, Path(gt=0, examples=[2])]) -> SueldosBase:
    for sb in db_sueldos_base:
        if sb["id"] == id:
            return SueldosBase(**sb)
    raise HTTPException(404, detail="Sueldo base no encontrado")

# ACTUALIZAR SUELDO BASE
@app.put("/actualizar-sueldo-base/{id}", tags=["SUELDOS"], response_model=SueldosBase, responses={
    404:{"description":"Sueldo base no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Sueldo base no encontrado"
                }
            }
        }}
})
def actualizar_sueldo_base(id: Annotated[int, Path(gt=0, examples=[2])], sueldo_base: SueldoBaseUpdate):
    for sb in db_sueldos_base:
        if sb["id"] == id:
            sb["cargo"] = sueldo_base.cargo
            sb["sueldo_base"] = sueldo_base.sueldo_base
            return sb
    raise HTTPException(404, detail="Sueldo base no encontrado")

# ACTUALIZAR PRECIO ESPECIAL
@app.put("/actualizar-precio-especial/{id}", tags=["SUELDOS"], response_model=PrecioEspecial, responses={
    404:{"description":"Precio especial no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Precio especial no encontrado"
                }
            }
        }}
})
def actualizar_precio_especial(id: Annotated[int, Path(gt=0, examples=[2])], precio_especial: PrecioEspecialUpdate):
    for p in db_precios_especiales:
        if p["id"] == id:
            p["descripcion"] = precio_especial.descripcion
            p["precio"] = precio_especial.precio
            return precio_especial
    raise HTTPException(404, detail="Precio especial no encontrado")

# --------------- AGENTES ---------------
# CREAR AGENTE
@app.post("/nuevo-empleado", tags=["AGENTES"] , response_model=list[AgenteModel])
def crear_empleado(agente: AgenteModel):
    for ag in db_agentes:
        if ag["id"] == agente.id:
            raise HTTPException(409, detail="El id ya existe")
    
    db_agentes.append(agente.model_dump())
    return db_agentes

# LISTAR AGENTES
@app.get("/agentes", tags=["AGENTES"], response_model=list[AgenteModel])
def listar_agentes():
    if len(db_agentes) < 1:
        raise HTTPException(404, detail="No hay agentes cargados")
    listado = []
    for agente in db_agentes:
        listado.append(agente)
    return listado

# OBTENER AGENTE POR ID
@app.get("/agentes/{id}", tags=["AGENTES"], response_model=AgenteModel , responses={
    404:{"description":"Agente no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Agente no encontrado"
                }
            }
        }}
})
def obtener_agente_por_id(id: Annotated[int, Path(gt=0, examples=[2])]):
    for agente in db_agentes:
        if agente["id"] == id:
            return agente
    raise HTTPException(404, detail="Agente no encontrado")


# ELIMINAR AGENTE
@app.delete("/agentes/{id}", tags=["AGENTES"], response_model=AgenteModel, responses={
    404:{"description":"Agente no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Agente no encontrado"
                }
            }
        }}
})
def eliminar_agente(id: Annotated[int, Path(gt=0, examples=[2])]):
    for agente in db_agentes:
        if agente["id"] == id:
            db_agentes.remove(agente)
            return agente
    raise HTTPException(404, detail="Agente no encontrado")

# --------------- PRESUPUESTO --------------- #

# LISTAR PRESUPUESTOS
@app.get("/saldos-presupuesto", tags=["PRESUPUESTO"], response_model=list[PresupuestoSobrante], responses={
    404:{"description":"No hay datos para listar",
        "content":{
            "application/json": {
                "example": {
                    "detail": "No hay datos para listar"
                }
            }
        }}
    })
def listar_presupuestos() -> list[PresupuestoSobrante]:
    if len(db_agentes) < 1:
        raise HTTPException(404, "No hay datos para listar")
    listado = []
    for ag in db_agentes:
        resultado = {
            "agente": f"{ag['apellido']} {ag['nombre']}",
            "pres_sobrante": ag["pres_asig"] - ag["pres_cons"]
        }
        listado.append(resultado)    
    return listado

# CALCULAR SUELDO
@app.get("/calcular-sueldo/{id}", tags=["PRESUPUESTO"], response_model=CalcularSueldo, responses={
    404:{"description":"Agente no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Agente no encontrado"
                }
            }
        }}
    })
def calcular_sueldo(id: Annotated[int, Path(gt=0, examples=[2])], cant_findes: Annotated[int, Query(gt=0, title="Cantidad Unidades Findes y Feriados" ,examples=[2]),], hs_adic: Annotated[int, Query(gt=0, title="Cantidad Hs Adiconales días habiles" ,examples=[2])]) -> CalcularSueldo:
    agente_encontrado = None
    for ag in db_agentes:
        if ag["id"] == id:
            agente_encontrado = ag
            break
    
    if not agente_encontrado:
        raise HTTPException(404, detail="Agente no encontrado")
    
    config_sueldo_base = next((sb for sb in db_sueldos_base if sb["cargo"] == agente_encontrado["cargo"]), None)
    if not config_sueldo_base:
        raise HTTPException(404, detail="Sueldo base para el cargo no asignado")
    sueldo_base = config_sueldo_base["sueldo_base"]

    config_precio_finde = next((p for p in db_precios_especiales if p["descripcion"] == PreciosEspecialesEnum.precio_turno_finde), None)
    config_precio_hs_ad = next((p for p in db_precios_especiales if p["descripcion"] == PreciosEspecialesEnum.precio_hora_adicional), None)
    if not config_precio_finde or not config_precio_hs_ad:
        raise HTTPException(404, detail="Precios especiales no asignados")
    
    precio_turno_finde = config_precio_finde["precio"]
    precio_hs_ad = config_precio_hs_ad["precio"]

    total_finde = cant_findes * precio_turno_finde
    total_hs_ad = hs_adic * precio_hs_ad
    total_a_cobrar = sueldo_base + total_finde + total_hs_ad

    return CalcularSueldo(
        Agente = f"{agente_encontrado['apellido']} {agente_encontrado['nombre']}",
        **{
            "Cargo": agente_encontrado["cargo"],
            "Sueldo_Base": sueldo_base,
            "tfsyf": total_finde,
            "Hs_Adicionales": total_hs_ad,
            "Total": total_a_cobrar
        }
    )

# IMPUTAR CONSUMO DE PRESUPUESTO
@app.put("/consumo-de-presupuesto/{id}/{cant_turnos}", tags=["PRESUPUESTO"], response_model=PresupuestoSobrante, responses={
    404:{"description":"Agente no encontrado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "Agente no encontrado"
                }
            }
        }},
    400:{"description":"No se puede imputar: supera el presupuesto asignado",
        "content":{
            "application/json": {
                "example": {
                    "detail": "No se puede imputar: supera el presupuesto asignado"
                }
            }
        }}
})
def imputar_turnos_pagados(id: Annotated[int, Path(gt=0, examples=[2])], cant_turnos: Annotated[int, Path(gt=0, title="Cantidad de turnos a imputar" ,examples=[2])]) -> PresupuestoSobrante:
    agente_encontrado = None
    for ag in db_agentes:
        if ag["id"] == id:
            agente_encontrado = ag
            break
    if not agente_encontrado:
        raise HTTPException(404, detail="Agente no encontrado")
    imputar_turnos_a_pagar = agente_encontrado["pres_cons"] + cant_turnos
    if imputar_turnos_a_pagar > agente_encontrado["pres_asig"]:
        raise HTTPException(400, detail="No se puede imputar: supera el presupuesto asignado")
    agente_encontrado["pres_cons"] = imputar_turnos_a_pagar
    return PresupuestoSobrante(
        agente=f"{agente_encontrado['apellido']} {agente_encontrado['nombre']}",
        pres_sobrante=agente_encontrado["pres_asig"] - agente_encontrado["pres_cons"]
    )




