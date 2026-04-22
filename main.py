from fastapi import FastAPI, Body


app = FastAPI()

app.title = "Giacri Facundo - Práctico 1: Crud en memoria con FastAPI"
app.summary =  "Consumo de Presupuesto"


agentes = [
    {"id": 1, "Apellido": "Arguello" ,"Nombre": "Abigail",  "Cargo": "Jefe de Turno", "Presupuesto Asignado": 36, "Presupuesto Consumido": 18},
    {"id": 2, "Apellido": "Ricca" ,"Nombre": "David",  "Cargo": "1° Ayudante", "Presupuesto Asignado": 36, "Presupuesto Consumido": 17},
    {"id": 3, "Apellido": "Rodriguez" ,"Nombre": "Gimena",  "Cargo": "2° Ayudante", "Presupuesto Asignado": 36, "Presupuesto Consumido": 19.75},
    {"id": 4, "Apellido": "Depetris" ,"Nombre": "Agustin",  "Cargo": "Agente", "Presupuesto Asignado": 24, "Presupuesto Consumido": 6},
    {"id": 5, "Apellido": "Diez" ,"Nombre": "Mario",  "Cargo": "Director", "Presupuesto Asignado": 42, "Presupuesto Consumido": 21},
]



# GET Obtener lista del saldo sobrante a consumir
# GET Por id obtener cuanto se le debe pagar de sueldo
# POST Crear nuevo empleado
# PUT Asignar presupuesto consumido
# DELETE Eliminar agente

@app.get("/presupuestos", tags=["PRESUPUESTO"])
def listar_presupuestos():
    listado = []
    for agente in agentes:
        resultado = {
            "Agente": f"{agente["Apellido"]} {agente["Nombre"]}",
            "Presupuesto Sobrante": agente["Presupuesto Asignado"] - agente["Presupuesto Consumido"]
        }
        listado.append(resultado)    
    return listado

@app.get("/agentes/{id}", tags=["AGENTES"])
def obtener_agente_por_id(id: int):
    for agente in agentes:
        if agente["id"] == id:
            return agente
    return {"msg": "agente no encontrado"}

@app.get("/calcular-sueldo/{id}", tags=["PRESUPUESTO"])
def calculadora_sueldos(id: int, cant_turnos_extras: int|float, hs_adic_habiles: int|float):
    sueldo_fijo = {
        "Director": 1000,
        "Subdirector": 800,
        "Jefe de Turno": 600,
        "1° Ayudante": 400,
        "2° Ayudante": 200,
        "Agente": 100,
    }
    
    precio_turno_finde = 500
    precio_hs_ad = 10
    for agente in agentes:
        if agente["id"] == id:
            sueldo_base = sueldo_fijo.get(agente["Cargo"], sueldo_fijo["Agente"])
            total_findes = cant_turnos_extras * precio_turno_finde
            total_hs_adic = hs_adic_habiles * precio_hs_ad 
            
            resultado = {
                "Agente": f"{agente["Apellido"]} {agente["Nombre"]}",
                "Cargo": agente["Cargo"],
                "Sueldo Base": sueldo_base,
                "Turnos Fin de Semana": total_findes,
                "Hs Adicionales": total_hs_adic,
                "Total a Cobrar": sueldo_base + total_findes + total_hs_adic
            }
            
            return resultado
        
    return "Persona No encontrada"
    
@app.post("/nuevo-empleado", tags=["AGENTES"])
def crear_empleado(id: int, apellido: str, nombre: str, cargo: str, pres_asig: int):
    for agente in agentes:
        if agente["id"] == id:
            return {"msg": "Ya existe un agente con ese id"}
    nuevo_empleado = {"id": id, "Apellido": apellido ,"Nombre": nombre,  "Cargo": cargo, "Presupuesto Asignado": pres_asig, "Presupuesto Consumido": 0}
    agentes.append(nuevo_empleado)
    return agentes

@app.put("/consumo-de-presupuesto", tags=["PRESUPUESTO"])
def imputar_turnos_pagados(id: int = Body(), cant_turnos: int|float = Body()):
    for agente in agentes:
        if agente["id"] == id:
            nuevo_consumo = agente["Presupuesto Consumido"] + cant_turnos
            if nuevo_consumo > agente["Presupuesto Asignado"]:
                return {"msg": "No se puede imputar: supera el presupuesto asignado"}
            agente["Presupuesto Consumido"] = nuevo_consumo
            return {
                "Agente": f"{agente["Apellido"]} {agente["Nombre"]}",
                "mensaje": "Turnos imputados correctamente", 
                "Presupuesto sobrante": agente["Presupuesto Asignado"] - agente["Presupuesto Consumido"]}
    return {"msg": "agente no encontrado"}
        
@app.delete("/eliminar-agente", tags=["AGENTES"])
def eliminar_agente(id: int):
    for agente in agentes:
        if agente["id"] == id:
            agentes.remove(agente)
            return agentes
    return {"msg": "agente no encontrado"}
            
            
            
            
                
                
                
                    