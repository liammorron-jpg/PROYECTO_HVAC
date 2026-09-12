from abc import ABC, abstractmethod

class EstadoHVAC(ABC):

    @abstractmethod
    def ejecutar(self):
        ...

class Apagado(EstadoHVAC):

    def ejecutar(self):
        return ("🔴 Se encuentra Apagado")

class Operando(EstadoHVAC):

    def ejecutar(self):
        return ("🟢 Se encuentra Operando")

class Mantenimiento(EstadoHVAC):

    def ejecutar(self):
        return ("🛠️ Se encuentra en Mantenimiento")
