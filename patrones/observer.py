"""
PATRÓN OBSERVER

Justificación en el contexto del proyecto HVAC:
-----------------------------------------------
El patrón Observer es esencial en este sistema HVAC porque permite notificar automáticamente
a múltiples componentes (pantallas, apps móviles, registros del sistema) cuando ocurren
eventos importantes, manteniendo un bajo acoplamiento entre el sistema y sus notificadores.

Problema que resuelve:
----------------------
Sin este patrón, el sistema tendría que llamar manualmente a cada componente que necesita
ser notificado, creando dependencias fuertes y haciendo difícil agregar nuevos destinos
de notificación sin modificar el código existente.

Alternativas consideradas:
---------------------------
1. Llamadas directas a cada componente: Acoplamiento fuerte, difícil de extender
2. Event system centralizado simple: Bueno pero menos estructurado para notificaciones
3. Observer: Elegido porque permite agregar/eliminar observadores dinámicamente y
   mantiene bajo acoplamiento entre el sujeto y sus observadores

Integración con el sistema:
---------------------------
Este patrón se integra a través de dos endpoints:
- PUT /habitaciones/{nombre}/observadores: Configura qué componentes recibirán notificaciones
- POST /habitaciones/{nombre}/evento: Envía eventos a todos los observadores configurados

Beneficios específicos:
-----------------------
- Notificación simultánea a múltiples componentes sin acoplamiento
- Facilidad para agregar nuevos tipos de observadores (ej: email, SMS)
- Flexibilidad para configurar diferentes combinaciones de observadores por habitación
- Separación clara entre generación de eventos y manejo de notificaciones

"""

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