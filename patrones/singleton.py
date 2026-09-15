"""
PATRÓN SINGLETON

Justificación en el contexto del proyecto HVAC:
-----------------------------------------------
El patrón Singleton es fundamental en este sistema porque garantiza que exista
un único Control Central HVAC que coordine todos los sistemas de monitoreo.
Esto es crítico para mantener la consistencia de datos y evitar duplicaciones.

Problema que resuelve:
----------------------
Sin este patrón, cada vez que se crea una instancia del Control Central se generaría
un nuevo registro de sistemas, causando inconsistencias donde diferentes partes del
sistema tendrían visiones diferentes del estado global.

Alternativas consideradas:
---------------------------
1. Variable global: Funcional pero no encapsulado, difícil de controlar accesos
2. Módulo singleton de Python: Bueno pero menos flexible para métodos de instancia
3. Singleton con __new__: Elegido porque proporciona control total sobre la instanciación
   y permite mantener estado interno (lista de sistemas registrados)

Integración con el sistema:
---------------------------
Este patrón se integra automáticamente cuando se crea un nuevo sistema HVAC
en la API, registrando cada habitación en el único control central accesible
mediante el endpoint GET /control-central.

Beneficios específicos:
-----------------------
- Centralización del registro de todos los sistemas HVAC
- Evita duplicación de sistemas en múltiples controles
- Permite consultas globales del estado del sistema
- Facilita la implementación de monitoreo centralizado

"""

from abc import ABC, abstractmethod

class ControlCentralHVAC:

    _instancia = None

    def __new__(cls):

        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.nombre = "Control Central HVAC"
            cls._instancia.sistemas = []

        return cls._instancia

    def registrar_sistema(self, sistema):

        if sistema not in self.sistemas:
            self.sistemas.append(sistema)

            return (
                f"✅ Sistema de {sistema.habitacion.nombre} "
                f"registrado en el Control Central HVAC"
            )

        return (
            f"⚠️ {sistema.habitacion.nombre} "
            f"ya está registrada"
        )

    def obtener_sistemas(self):

        return [
            {
                "habitacion": sistema.habitacion.nombre,
                "piso": sistema.habitacion.piso,
                "equipo": sistema.equipo.__class__.__name__
            }
            for sistema in self.sistemas
        ]

    def obtener_info(self):

        return {
            "nombre": self.nombre,
            "cantidad_sistemas": len(self.sistemas),
            "habitaciones": [ 
                sistema.habitacion.nombre
                for sistema in self.sistemas
            ]
        }