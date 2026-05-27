from fastapi import FastAPI, Body, HTTPException, Path
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

db_sueldos_base = []

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

class SueldoBaseUpdate(BaseModel):
    cargo: CargosEnum
    sueldo_base: Annotated[int, Field(gt=0, examples=[1000])]

# --------------- SUELDOS BASE ---------------
# CREAR SUELDO BASE
@app.post("/cargar-sueldo", tags=["SUELDOS BASE"], response_model=list[SueldosBase], responses={
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
                    "detail": "El cargo no es válido."
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

# LISTAR SUELDOS BASE
@app.get("/sueldos_base", tags=["SUELDOS BASE"], responses={
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

# OBTENER SUELDO BASE POR ID
@app.get("/sueldo-base/{id}", response_model=SueldosBase, tags=["SUELDOS BASE"], responses={
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
            return sb
    raise HTTPException(404, detail="Sueldo base no encontrado")

# ACTUALIZAR SUELDO BASE
@app.put("/actualizar-sueldo-base/{id}", tags=["SUELDOS BASE"], response_model=SueldosBase, responses={
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


# @app.get("/presupuestos", tags=["PRESUPUESTO"])
# def listar_presupuestos():
#     listado = []
#     for agente in agentes:
#         resultado = {
#             "Agente": f"{agente["Apellido"]} {agente["Nombre"]}",
#             "Presupuesto Sobrante": agente["Presupuesto Asignado"] - agente["Presupuesto Consumido"]
#         }
#         listado.append(resultado)    
#     return listado








# @app.get("/calcular-sueldo/{id}", tags=["PRESUPUESTO"])
# def calculadora_sueldos(id: int, cant_turnos_extras: int|float, hs_adic_habiles: int|float):
#     sueldo_fijo = {
#         "Director": 1000,
#         "Subdirector": 800,
#         "Jefe de Turno": 600,
#         "1° Ayudante": 400,
#         "2° Ayudante": 200,
#         "Agente": 100,
#     }
    
#     precio_turno_finde = 500
#     precio_hs_ad = 10
#     for agente in agentes:
#         if agente["id"] == id:
#             sueldo_base = sueldo_fijo.get(agente["Cargo"], sueldo_fijo["Agente"])
#             total_findes = cant_turnos_extras * precio_turno_finde
#             total_hs_adic = hs_adic_habiles * precio_hs_ad 
            
#             resultado = {
#                 "Agente": f"{agente["Apellido"]} {agente["Nombre"]}",
#                 "Cargo": agente["Cargo"],
#                 "Sueldo Base": sueldo_base,
#                 "Turnos Fin de Semana": total_findes,
#                 "Hs Adicionales": total_hs_adic,
#                 "Total a Cobrar": sueldo_base + total_findes + total_hs_adic
#             }
            
#             return resultado
        
#     return "Persona No encontrada"
    

# @app.put("/consumo-de-presupuesto", tags=["PRESUPUESTO"])
# def imputar_turnos_pagados(id: int = Body(), cant_turnos: int|float = Body()):
#     for agente in agentes:
#         if agente["id"] == id:
#             nuevo_consumo = agente["Presupuesto Consumido"] + cant_turnos
#             if nuevo_consumo > agente["Presupuesto Asignado"]:
#                 return {"msg": "No se puede imputar: supera el presupuesto asignado"}
#             agente["Presupuesto Consumido"] = nuevo_consumo
#             return {
#                 "Agente": f"{agente["Apellido"]} {agente["Nombre"]}",
#                 "mensaje": "Turnos imputados correctamente", 
#                 "Presupuesto sobrante": agente["Presupuesto Asignado"] - agente["Presupuesto Consumido"]}
#     return {"msg": "agente no encontrado"}