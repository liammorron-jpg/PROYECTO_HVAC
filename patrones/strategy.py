from abc import ABC, abstractmethod

class EstrategiaClimatizacion(ABC):

    @abstractmethod
    def ejecutar(self):
        ...

class EstrategiaEco(EstrategiaClimatizacion):

    def ejecutar(self):
        return {
            "modo": "ECO", "temperatura_objetivo": 25
        }

class EstrategiaConfort(EstrategiaClimatizacion):

    def ejecutar(self):
        return {
            "modo": "CONFORT", "temperatura_objetivo": 22
        }

class EstrategiaTurbo(EstrategiaClimatizacion):

    def ejecutar(self):
        return {
            "modo": "TURBO", "temperatura_objetivo": 17
        }

class SistemaClimatizacion:

    def __init__(self, estrategia=None):
        self.estrategia = (
            estrategia or EstrategiaEco()
        )

    def cambiar_estrategia(self, nueva_estrategia):
        self.estrategia = nueva_estrategia

    def climatizar(self):
        return self.estrategia.ejecutar()