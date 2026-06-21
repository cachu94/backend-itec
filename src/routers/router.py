from fastapi import APIRouter, HTTPException, Path, Query
from src.schemas.models import VehiculoBase, VehiculoResponse

router = APIRouter()