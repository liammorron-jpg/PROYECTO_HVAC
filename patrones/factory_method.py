"""El patrón Factory Method es esencial en este sistema HVAC porque resuelve el problema de crear diferentes tipos de equipos (aire acondicionado, calefactor, ventilador) sin que el código cliente dependa de clases concretas.

Problema que resuelve:
----------------------
Sin este patrón, el código tendría que usar condicionales (if/elif) para decidir qué
clase instanciar, lo que viola el principio Open/Closed y hace difícil agregar nuevos
tipos de equipos en el futuro.

Integración con el sistema:
---------------------------
Este patrón se integra con la API a través del endpoint PUT /habitaciones/{nombre}/equipo,
permitiendo cambiar dinámicamente el tipo de equipo HVAC de una habitación."""

from abc import ABC, abstractmethod

class HVACDevice(ABC):

    def __init__(self):
        self.encendido = False

    @abstractmethod
    def encender(self):
        pass

    def apagar(self):
        self.encendido = False
        return f"{self.__class__.__name__} apagado"

    def obtener_estado(self):
        return "Encendido" if self.encendido else "Apagado"

class AireAcondicionado(HVACDevice):

    def encender(self):
        self.encendido = True
        return "❄️ Aire acondicionado encendido"

class Calefactor(HVACDevice):

    def encender(self):
        self.encendido = True
        return "🔥 Calefactor encendido"

class Ventilador(HVACDevice):

    def encender(self):
        self.encendido = True
        return "💨 Ventilador encendido"
    
class HVACFactory(ABC):

    @abstractmethod
    def crear_equipo(self):
        pass

class FabricaAire(HVACFactory):

    def crear_equipo(self):
        return AireAcondicionado()

class FabricaCalefactor(HVACFactory):

    def crear_equipo(self):
        return Calefactor()

class FabricaVentilador(HVACFactory):

    def crear_equipo(self):
        return Ventilador()
