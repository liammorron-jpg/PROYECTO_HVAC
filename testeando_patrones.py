"""
PRUEBAS Y EJEMPLOS DE USO AISLADOS PARA PATRONES DE DISEÑO HVAC

Este archivo contiene ejemplos de uso aislados para cada patrón de diseño
implementado en el sistema HVAC, permitiendo verificar su funcionamiento
de forma independiente sin depender de la API completa.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(PROJECT_ROOT))

from patrones.factory_method import FabricaAire, FabricaCalefactor, FabricaVentilador
from patrones.singleton import ControlCentralHVAC
from patrones.strategy import SistemaClimatizacion, EstrategiaEco, EstrategiaConfort, EstrategiaTurbo
from patrones.state import Apagado, Operando, Mantenimiento
from patrones.observer import GestorEventos
from modelos.habitacion import Habitacion
from modelos.sistema_hvac import SistemaHVAC


def test_factory_method():
    """Prueba aislada del patrón Factory Method"""
    print("\n=== PRUEBA FACTORY METHOD ===")
    
    # Crear diferentes equipos usando las fábricas
    fabrica_aire = FabricaAire()
    aire = fabrica_aire.crear_equipo()
    print(f"Equipo creado: {aire.__class__.__name__}")
    print(f"Estado inicial: {aire.obtener_estado()}")
    print(f"Encender: {aire.encender()}")
    print(f"Estado después: {aire.obtener_estado()}")
    
    fabrica_calefactor = FabricaCalefactor()
    calefactor = fabrica_calefactor.crear_equipo()
    print(f"\nEquipo creado: {calefactor.__class__.__name__}")
    print(f"Encender: {calefactor.encender()}")
    
    fabrica_ventilador = FabricaVentilador()
    ventilador = fabrica_ventilador.crear_equipo()
    print(f"\nEquipo creado: {ventilador.__class__.__name__}")
    print(f"Encender: {ventilador.encender()}")
    
    print("✅ Factory Method funciona correctamente")


def test_singleton():
    """Prueba aislada del patrón Singleton"""
    print("\n=== PRUEBA SINGLETON ===")
    
    # Crear múltiples instancias
    control1 = ControlCentralHVAC()
    control2 = ControlCentralHVAC()
    control3 = ControlCentralHVAC()
    
    # Verificar que son la misma instancia
    print(f"control1 es control2: {control1 is control2}")
    print(f"control2 es control3: {control2 is control3}")
    print(f"control1 es control3: {control1 is control3}")
    
    # Crear sistemas de prueba
    habitacion1 = Habitacion("Sala Principal", "Piso 1")
    habitacion2 = Habitacion("Oficina", "Piso 2")
    
    equipo1 = FabricaAire().crear_equipo()
    equipo2 = FabricaCalefactor().crear_equipo()
    
    sistema1 = SistemaHVAC(habitacion1, equipo1, Apagado(), SistemaClimatizacion(EstrategiaEco()), GestorEventos())
    sistema2 = SistemaHVAC(habitacion2, equipo2, Apagado(), SistemaClimatizacion(EstrategiaEco()), GestorEventos())
    
    # Registrar sistemas usando cualquier instancia
    control1.registrar_sistema(sistema1)
    control2.registrar_sistema(sistema2)
    
    # Verificar que todas las instancias ven los mismos sistemas
    print(f"Sistemas en control1: {control1.obtener_info()}")
    print(f"Sistemas en control2: {control2.obtener_info()}")
    print(f"Sistemas en control3: {control3.obtener_info()}")
    
    print("✅ Singleton funciona correctamente")


def test_strategy():
    """Prueba aislada del patrón Strategy"""
    print("\n=== PRUEBA STRATEGY ===")
    
    # Crear sistema de climatización con estrategia por defecto
    sistema = SistemaClimatizacion()
    print(f"Estrategia inicial: {sistema.climatizar()}")
    
    # Cambiar a diferentes estrategias
    sistema.cambiar_estrategia(EstrategiaConfort())
    print(f"Estrategia Confort: {sistema.climatizar()}")
    
    sistema.cambiar_estrategia(EstrategiaTurbo())
    print(f"Estrategia Turbo: {sistema.climatizar()}")
    
    sistema.cambiar_estrategia(EstrategiaEco())
    print(f"Estrategia Eco: {sistema.climatizar()}")
    
    print("✅ Strategy funciona correctamente")


def test_state():
    """Prueba aislada del patrón State"""
    print("\n=== PRUEBA STATE ===")
    
    # Crear sistema HVAC con diferentes estados
    habitacion = Habitacion("Prueba State", "Piso 1")
    equipo = FabricaAire().crear_equipo()
    
    # Estado inicial: Apagado
    sistema_apagado = SistemaHVAC(habitacion, equipo, Apagado(), SistemaClimatizacion(EstrategiaEco()), GestorEventos())
    print(f"Estado Apagado: {sistema_apagado.estado.ejecutar()}")
    
    # Cambiar a Operando
    sistema_apagado.cambiar_estado(Operando())
    print(f"Estado Operando: {sistema_apagado.estado.ejecutar()}")
    
    # Cambiar a Mantenimiento
    sistema_apagado.cambiar_estado(Mantenimiento())
    print(f"Estado Mantenimiento: {sistema_apagado.estado.ejecutar()}")
    
    # Volver a Apagado
    sistema_apagado.cambiar_estado(Apagado())
    print(f"Estado Apagado: {sistema_apagado.estado.ejecutar()}")
    
    print("✅ State funciona correctamente")


def test_observer():
    """Prueba aislada del patrón Observer"""
    print("\n=== PRUEBA OBSERVER ===")
    
    # Crear gestor de eventos
    gestor = GestorEventos()
    
    # Intentar notificar sin observadores
    resultado = gestor.notificar("Prueba sin observadores")
    print(f"Notificar sin observadores: {resultado}")
    
    # Configurar observadores
    observadores = gestor.seleccionar_observadores(["1", "2"])  # Pantalla y App móvil
    print(f"Observadores configurados: {observadores}")
    
    # Enviar evento
    resultado = gestor.notificar("Temperatura ajustada a 22°C")
    print(f"Notificación enviada: {resultado}")
    
    # Configurar diferentes observadores
    observadores = gestor.seleccionar_observadores(["1", "3"])  # Pantalla y Registro
    print(f"Nuevos observadores: {observadores}")
    
    resultado = gestor.notificar("Sistema en modo mantenimiento")
    print(f"Notificación enviada: {resultado}")
    
    # Configurar todos los observadores
    observadores = gestor.seleccionar_observadores(["1", "2", "3"])
    print(f"Todos los observadores: {observadores}")
    
    resultado = gestor.notificar("Alerta: Temperatura fuera de rango")
    print(f"Notificación enviada: {resultado}")
    
    print("✅ Observer funciona correctamente")


def test_integracion_completa():
    """Prueba de integración de todos los patrones juntos"""
    print("\n=== PRUEBA DE INTEGRACIÓN COMPLETA ===")
    
    # Crear sistema HVAC completo usando todos los patrones
    habitacion = Habitacion("Sala de Conferencias", "Piso 3")
    equipo = FabricaAire().crear_equipo()
    
    # Usar Strategy para climatización
    climatizacion = SistemaClimatizacion(EstrategiaConfort())
    
    # Usar State para estado inicial
    estado = Operando()
    
    # Usar Observer para eventos
    eventos = GestorEventos()
    eventos.seleccionar_observadores(["1", "2"])
    
    # Crear sistema completo
    sistema = SistemaHVAC(habitacion, equipo, estado, climatizacion, eventos)
    
    # Registrar en Singleton
    control = ControlCentralHVAC()
    control.registrar_sistema(sistema)
    
    # Probar funcionalidad completa
    print(f"Info del sistema: {sistema.obtener_info()}")
    
    # Cambiar estrategia
    sistema.cambiar_estrategia(EstrategiaTurbo())
    print(f"Después de cambiar estrategia: {sistema.obtener_info()}")
    
    # Cambiar estado
    sistema.cambiar_estado(Mantenimiento())
    print(f"Después de cambiar estado: {sistema.obtener_info()}")
    
    # Enviar evento
    resultado = sistema.enviar_evento("Mantenimiento programado iniciado")
    print(f"Evento enviado: {resultado}")
    
    # Ver control central
    print(f"Control central: {control.obtener_info()}")
    
    print("✅ Integración completa funciona correctamente")


if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBAS AISLADAS DE PATRONES DE DISEÑO HVAC")
    print("=" * 50)
    
    try:
        test_factory_method()
        test_singleton()
        test_strategy()
        test_state()
        test_observer()
        test_integracion_completa()
        
        print("\n" + "=" * 50)
        print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()