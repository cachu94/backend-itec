from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from src.database import get_db
from src import models
from src.schemas.schemas import Movil, MovilUpdate

router = APIRouter()

db_vehiculos = [
    {
        "id": 1,
        "patente": "AA134JP",
        "marca": "Renault",
        "modelo": "Clio",
        "km_actual": 150100,
        "estado": "Disponible",
    },
    {
        "id": 2,
        "patente": "AG546JL",
        "marca": "Nissan",
        "modelo": "Frontier",
        "halcon": 18,
        "km_actual": 50187,
        "estado": "Disponible",
    },
    {
        "id": 3,
        "patente": "AF913WN",
        "marca": "Peugeot",
        "modelo": "208",
        "halcon": 10,
        "km_actual": 119980,
        "estado": "En Mantenimiento",
    }
]  # Simulación de base de datos en memoria

# Obtenemos todos los vehículos
@router.get("/", response_model=List[Movil])
async def Obtener_moviles(db: Session = Depends(get_db)) -> List[Movil]:
    return db.query(models.Movil).all()

# Obtenemos un vehículo por su ID
@router.get("/{id}", response_model=Movil)
async def obtener_movil_id(id: Annotated[int, Path(ge=1, description="ID del vehículo")], db: Session = Depends(get_db)) -> Movil:
    db_movil = db.query(models.Movil).filter(models.Movil.id == id).first()

    if not db_movil:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    return db_movil

# Creación o alta de un nuevo vehículo
@router.post("/", status_code=201, response_model=Movil)
async def agregar_movil(movil: MovilUpdate, db: Session = Depends(get_db)) -> Movil:
    db_movil = models.Movil(
        patente = movil.patente,
        marca = movil.marca,
        modelo = movil.modelo,
        km_inicial = movil.km_inicial,
        estado = movil.estado,
    )

    db.add(db_movil)
    db.commit()
    db.refresh(db_movil)

    return db_movil

# Actualización de estado y kilometraje de un vehículo
@router.put("/{id}", response_model=Movil)
async def update_vehiculo(id: Annotated[int, Path(ge=1, description="ID del vehículo")], movil: MovilUpdate ,db: Session = Depends(get_db)) -> Movil:
    db_movil = db.query(models.Movil).filter(models.Movil.id == id).first()

    db_movil.patente = movil.patente
    db_movil.marca = movil.marca
    db_movil.modelo = movil.modelo
    db_movil.km_inicial = movil.km_inicial
    db_movil.estado = movil.estado

    db.commit()
    db.refresh(db_movil)

    return db_movil

    


# Eliminación de un vehículo de la flota
@router.delete("/{id}", response_model=list[Movil])
async def eliminar_movil(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    db_movil = db.query(models.Movil).filter(models.Movil.id == id).first()

    if not db_movil:
        raise HTTPException(status_code=404, detail="Movil no encontrado")

    db.delete(db_movil)
    db.commit()

    return db.query(models.Movil).all()