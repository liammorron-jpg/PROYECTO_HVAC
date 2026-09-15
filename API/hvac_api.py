import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

class ObservadoresRequest(BaseModel):
    opciones: list

class EventoRequest(BaseModel):
    mensaje: str

from modelos.habitacion import Habitacion
from modelos.sistema_hvac import SistemaHVAC
from patrones.factory_method import FabricaAire, FabricaCalefactor, FabricaVentilador
from patrones.singleton import ControlCentralHVAC
from patrones.strategy import SistemaClimatizacion, EstrategiaEco, EstrategiaConfort, EstrategiaTurbo
from patrones.observer import GestorEventos
from patrones.state import Apagado, Operando, Mantenimiento


app = FastAPI(
    title="Sistema de Monitoreo HVAC",
    description="Monitoreo y gestión de sistemas HVAC",
    version="2.0.0"
)

sistemas = {}

BASE_DIR = Path(__file__).resolve().parent
PANEL_HTML = BASE_DIR / "panel_hvac.html"
LOGO_SVG = BASE_DIR / "logo_hvac.svg"


def crear_equipo(tipo: str):
    fabricas = {
        "aire": FabricaAire,
        "calefactor": FabricaCalefactor,
        "ventilador": FabricaVentilador
    }

    fabrica = fabricas.get(tipo.lower())

    if not fabrica:
        raise HTTPException(
            status_code=400,
            detail="Equipo válido: aire, calefactor o ventilador"
        )

    return fabrica().crear_equipo()


def obtener_sistema(nombre: str):
    sistema = sistemas.get(nombre.casefold())

    if not sistema:
        raise HTTPException(
            status_code=404,
            detail="La habitación o zona no ha sido registrada"
        )

    return sistema


def obtener_o_crear_sistema(
    nombre: str,
    piso: Optional[str] = None,
    equipo: Optional[str] = None
):
    nombre = nombre.strip()

    if not nombre:
        raise HTTPException(
            status_code=400,
            detail="Ingrese habitación o zona"
        )

    clave = nombre.casefold()

    if clave not in sistemas:
        equipo_creado = crear_equipo(equipo or "aire")
        # El estado inicial depende de si el equipo está encendido
        estado_inicial = Operando() if equipo_creado.encendido else Apagado()

        sistema = SistemaHVAC(
            Habitacion(nombre, piso),
            equipo_creado,
            estado_inicial,
            SistemaClimatizacion(EstrategiaEco()),
            GestorEventos()
        )

        sistemas[clave] = sistema
        ControlCentralHVAC().registrar_sistema(sistema)

    else:
        sistema = sistemas[clave]

        if piso is not None:
            sistema.habitacion.piso = piso

        if equipo is not None:
            sistema.equipo = crear_equipo(equipo)
            # Actualizar el estado según el nuevo equipo
            sistema.estado = Operando() if sistema.equipo.encendido else Apagado()

    return sistema


def resumir_sistema(sistema):
    info = sistema.obtener_info()

    return {
        "habitacion": info["habitacion"],
        "piso": info["piso"],
        "equipo": info["equipo"],
        "equipo_encendido": info["equipo_encendido"],
        "estado_equipo": info["estado_equipo"],
        "estado": info["estado"],
        "modo": info["climatizacion"]["modo"],
        "temperatura_objetivo": info["climatizacion"]["temperatura_objetivo"]
    }


@app.get("/")
def inicio():
    return {
        "proyecto": "Sistema de Monitoreo HVAC",
        "estado": "API funcionando correctamente",
        "version": "2.0.0",
        "panel": "/panel",
        "documentacion": "/docs"
    }


@app.get("/habitaciones/{nombre}")
def consultar_habitacion(
    nombre: str,
    piso: Optional[str] = None,
    equipo: Optional[str] = None
):
    return resumir_sistema(
        obtener_o_crear_sistema(nombre, piso, equipo)
    )


@app.get("/habitaciones")
def listar_habitaciones():
    zonas = [
        resumir_sistema(sistema)
        for sistema in sistemas.values()
    ]

    return {
        "total": len(zonas),
        "zonas": zonas
    }


@app.put("/habitaciones/{nombre}/equipo")
def cambiar_equipo(nombre: str, equipo: str):
    sistema = obtener_sistema(nombre)
    sistema.equipo = crear_equipo(equipo)

    return {
        "mensaje": f"Equipo cambiado a {sistema.equipo.__class__.__name__}",
        "sistema": resumir_sistema(sistema)
    }

@app.put("/habitaciones/{nombre}/equipo/estado")
def cambiar_estado_equipo(nombre: str, encendido: bool):
    sistema = obtener_sistema(nombre)

    return {
        "mensaje": sistema.cambiar_estado_equipo(encendido),
        "sistema": resumir_sistema(sistema)
    }

@app.put("/habitaciones/{nombre}/estrategia")
def cambiar_estrategia(nombre: str, estrategia: str):
    sistema = obtener_sistema(nombre)

    estrategias = {
        "eco": EstrategiaEco(),
        "confort": EstrategiaConfort(),
        "turbo": EstrategiaTurbo()
    }

    estrategia_obj = estrategias.get(estrategia.lower())

    if not estrategia_obj:
        raise HTTPException(
            status_code=400,
            detail="Estrategia válida: eco, confort o turbo"
        )

    sistema.cambiar_estrategia(estrategia_obj)

    return {
        "mensaje": f"Estrategia cambiada a {estrategia.upper()}",
        "sistema": resumir_sistema(sistema)
    }

@app.put("/habitaciones/{nombre}/estado")
def cambiar_estado_sistema(nombre: str, estado: str):
    sistema = obtener_sistema(nombre)

    estados = {
        "apagado": Apagado(),
        "operando": Operando(),
        "mantenimiento": Mantenimiento()
    }

    estado_obj = estados.get(estado.lower())

    if not estado_obj:
        raise HTTPException(
            status_code=400,
            detail="Estado válido: apagado, operando o mantenimiento"
        )

    mensaje = sistema.cambiar_estado(estado_obj)

    return {
        "mensaje": mensaje,
        "sistema": resumir_sistema(sistema)
    }

@app.put("/habitaciones/{nombre}/observadores")
def configurar_observadores(nombre: str, request: ObservadoresRequest):
    sistema = obtener_sistema(nombre)

    resultado = sistema.seleccionar_observadores(request.opciones)

    return {
        "mensaje": "Observadores configurados",
        "observadores": resultado,
        "sistema": resumir_sistema(sistema)
    }

@app.post("/habitaciones/{nombre}/evento")
def enviar_evento(nombre: str, request: EventoRequest):
    sistema = obtener_sistema(nombre)

    resultado = sistema.enviar_evento(request.mensaje)

    return {
        "mensaje": "Evento enviado",
        "resultado": resultado,
        "sistema": resumir_sistema(sistema)
    }

@app.get("/control-central")
def consultar_control_central():
    return ControlCentralHVAC().obtener_info()

@app.get("/panel", include_in_schema=False)
def panel():
    if not PANEL_HTML.exists():
        raise HTTPException(500, "No se encontró panel_hvac.html")

    return FileResponse(PANEL_HTML)

@app.get("/logo_hvac.svg", include_in_schema=False)
def logo():
    if not LOGO_SVG.exists():
        raise HTTPException(404, "No se encontró el logo HVAC")

    return FileResponse(LOGO_SVG, media_type="image/svg+xml")

if __name__ == "__main__":

    print(
        "\n"
        "========================================\n"
        "     SISTEMA DE MONITOREO HVAC\n"
        "========================================\n"
        "API:      http://127.0.0.1:8001\n"
        "PANEL:    http://127.0.0.1:8001/panel\n"
        "SWAGGER:  http://127.0.0.1:8001/docs\n"
        "========================================\n"
    )

  