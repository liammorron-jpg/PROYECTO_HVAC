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
