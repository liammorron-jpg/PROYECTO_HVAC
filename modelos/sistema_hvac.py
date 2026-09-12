class SistemaHVAC:

    def __init__(self, habitacion, equipo, estado, climatizacion, eventos):
        self.habitacion = habitacion
        self.equipo = equipo
        self.estado = estado
        self.climatizacion = climatizacion
        self.eventos = eventos


    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

        return (f"{self.habitacion.nombre} cambió a " f"{self.estado.ejecutar()}")

    def cambiar_estrategia(self, nueva_estrategia):
        self.climatizacion.cambiar_estrategia(nueva_estrategia)

        return (self.climatizacion.climatizar())

    def seleccionar_observadores(self, opciones):
        return (self.eventos.seleccionar_observadores(opciones))

    def enviar_evento(self, mensaje):
        mensaje = str(mensaje).strip()

        if not mensaje:
            return { "error": "El mensaje no puede estar vacío" }

        return self.eventos.notificar(mensaje)

    def cambiar_estado_equipo(self, encendido):
        if encendido:
            return self.equipo.encender()

        return self.equipo.apagar()

    def obtener_info(self):

        return {
            "habitacion": self.habitacion.nombre,
            "piso": self.habitacion.piso,
            "equipo": self.equipo.__class__.__name__,
            "equipo_encendido": self.equipo.encendido,
            "estado_equipo": self.equipo.obtener_estado(),
            "estado": self.estado.ejecutar(),
            "climatizacion": self.climatizacion.climatizar()
        }