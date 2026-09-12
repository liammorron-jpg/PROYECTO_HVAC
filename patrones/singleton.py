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