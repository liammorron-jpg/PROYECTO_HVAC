from abc import ABC, abstractmethod

class Observador(ABC):

    @abstractmethod
    def actualizar(self, mensaje):
        ...

class Pantalla(Observador):

    def actualizar(self, mensaje):
        return f"📺 Pantalla: {mensaje}"

class AppMovil(Observador):

    def actualizar(self, mensaje):
        return f"📱 App móvil: {mensaje}"

class RegistroSistema(Observador):

    def actualizar(self, mensaje):
        return f"📝 Registro: {mensaje}"

class GestorEventos:

    def __init__(self):
        self.observadores = []

    def seleccionar_observadores(self, opciones):
        disponibles = {"1": Pantalla, "2": AppMovil, "3": RegistroSistema}

        opciones_validas = {
            opcion.strip()
            for opcion in opciones
            if opcion.strip() in disponibles
        }

        self.observadores = [
            disponibles[opcion]()
            for opcion in opciones_validas
        ]

        if not self.observadores:
            return {
                "error": "No se seleccionó ningún observador válido"
            }

        return [
            observador.__class__.__name__
            for observador in self.observadores
        ]

    def notificar(self, mensaje):

        if not self.observadores:
            return {
                "error": "No hay observadores seleccionados"
            }

        return [
            observador.actualizar(mensaje)
            for observador in self.observadores
        ]