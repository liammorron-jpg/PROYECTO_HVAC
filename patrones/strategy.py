"""
PATRÓN STRATEGY

Justificación en el contexto del proyecto HVAC:
-----------------------------------------------
El patrón Strategy es esencial en este sistema HVAC porque permite cambiar dinámicamente
el algoritmo de control de temperatura según las necesidades del momento (ahorro de energía,
confort máximo, o enfriamiento rápido) sin modificar la estructura del sistema.

Problema que resuelve:
----------------------
Sin este patrón, el código tendría que usar condicionales complejos para decidir qué
algoritmo de climatización aplicar, haciendo el código difícil de mantener y extendiendo
las clases con comportamientos que deberían ser intercambiables.

Alternativas consideradas:
---------------------------
1. Condicionales if/elif: Código rígido, difícil de agregar nuevas estrategias
2. Herencia múltiple: Complejo y poco mantenible para comportamientos intercambiables
3. Strategy: Elegido porque permite intercambiar algoritmos en tiempo de ejecución
   y facilitar la agregación de nuevas estrategias sin modificar código existente

Integración con el sistema:
---------------------------
Este patrón se integra a través del endpoint PUT /habitaciones/{nombre}/estrategia,
permitiendo cambiar dinámicamente entre modos ECO, CONFORT y TURBO según las necesidades.

Beneficios específicos:
-----------------------
- Flexibilidad para adaptarse a diferentes condiciones ambientales
- Facilidad para agregar nuevos modos de operación (ej: nocturno, vacaciones)
- Separación clara entre lógica de control y implementación de estrategias
- Testabilidad mejorada al poder probar cada estrategia de forma aislada

"""

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