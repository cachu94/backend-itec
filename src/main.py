from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.router import router as vehiculos_router

app = FastAPI(
    title="API de Gestión de Vehículos GLP",
    description="API para el control de entrega, devolución y mantenimiento de vehículos GLP.",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehiculos_router)
