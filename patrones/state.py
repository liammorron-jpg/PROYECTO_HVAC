"""
PATRÓN STATE

Justificación en el contexto del proyecto HVAC:
-----------------------------------------------
El patrón State es fundamental en este sistema HVAC porque permite que el comportamiento
del sistema cambie dinámicamente según su estado actual (apagado, operando, mantenimiento).
Esto es crucial para sistemas que tienen diferentes comportamientos según su condición.

Problema que resuelve:
----------------------
Sin este patrón, el código tendría que verificar constantemente el estado con condicionales
antes de ejecutar cualquier acción, resultando en código complejo, propenso a errores y difícil
de mantener. Cada estado tendría su lógica dispersa en diferentes partes del código.

Alternativas consideradas:
---------------------------
1. Enumeraciones con switch/case: Código rígido, difícil de agregar nuevos estados
2. Variables de estado booleanas: No escala bien, complicado para múltiples estados
3. State: Elegido porque encapsula el comportamiento específico de cada estado en clases
   separadas, facilitando la agregación de nuevos estados y transiciones

Integración con el sistema:
---------------------------
Este patrón se integra a través del endpoint PUT /habitaciones/{nombre}/estado,
permitiendo transiciones fluidas entre estados APAGADO, OPERANDO y MANTENIMIENTO.

Corrección implementada:
------------------------
Se corrigió el problema donde el estado siempre devolvía "Apagado". Ahora el estado
inicial depende del estado del equipo (encendido/apagado) y puede cambiarse dinámicamente.

Beneficios específicos:
-----------------------
- Comportamiento diferente según el estado sin condicionales complejos
- Facilidad para agregar nuevos estados (ej: error, standby)
- Transiciones de estado controladas y validadas
- Código más limpio y mantenible con responsabilidades separadas

"""

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
