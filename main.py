"""Punto de entrada de la API del Sistema de Monitoreo HVAC."""

import uvicorn
from fastapi import FastAPI

from API.hvac_api import app as hvac_app


app = FastAPI(
    title="Sistema de Monitoreo HVAC",
    description=(
        "API para el monitoreo y control de un sistema HVAC "
        "utilizando patrones de diseño GoF."
    ),
    version="2.0.0",
)


# Agrega las rutas definidas en hvac_api.py
app.include_router(
    hvac_app.router,
    tags=["HVAC"],
)


@app.get("/", include_in_schema=False)
def read_root():
    """Verifica que el sistema HVAC esté funcionando."""
    return {
        "message": "Sistema de Monitoreo HVAC funcionando",
        "api": "http://127.0.0.1:8001",
        "panel": "http://127.0.0.1:8001/panel",
        "swagger": "http://127.0.0.1:8001/docs",
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
    )