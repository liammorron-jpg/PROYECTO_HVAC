# DOCUMENTACIÓN DE DIAGRAMAS UML - SISTEMA HVAC

Este documento explica los diagramas UML implementados en el proyecto HVAC para cada patrón de diseño.

## 1. FACTORY METHOD

### Propósito del Diagrama
El diagrama UML de Factory Method muestra la estructura de creación de objetos donde las subclases deciden qué clase instanciar. En el contexto HVAC, permite crear diferentes tipos de equipos (aire acondicionado, calefactor, ventilador) sin acoplar el código a clases concretas.

### Componentes del Diagrama
- **HVACDevice (Abstract Product)**: Clase abstracta que define la interfaz común para todos los dispositivos HVAC
- **AireAcondicionado, Calefactor, Ventilador (Concrete Products)**: Implementaciones concretas de dispositivos
- **HVACFactory (Abstract Creator)**: Clase abstracta que declara el método factory
- **FabricaAire, FabricaCalefactor, FabricaVentilador (Concrete Creators)**: Fábricas concretas que crean productos específicos

### Relaciones
- **Herencia**: Los productos concretos heredan de HVACDevice
- **Herencia**: Las fábricas concretas heredan de HVACFactory
- **Creación**: Cada fábrica concreta crea una instancia de su producto correspondiente

### Beneficios en el Sistema HVAC
- Permite agregar nuevos tipos de equipos sin modificar el código existente
- Facilita el cambio dinámico de equipos mediante el endpoint PUT /habitaciones/{nombre}/equipo
- Mantiene bajo acoplamiento entre el código cliente y las clases de equipos

---

## 2. SINGLETON

### Propósito del Diagrama
El diagrama UML de Singleton muestra cómo garantizar que una clase tenga una única instancia y proporcionar un punto de acceso global a ella. En el contexto HVAC, esto asegura un único Control Central que coordina todos los sistemas.

### Componentes del Diagrama
- **ControlCentralHVAC**: Clase que implementa el patrón Singleton
- **_instancia (atributo estático)**: Variable de clase que mantiene la única instancia
- **__new__ (método estático)**: Método que controla la creación de la instancia única
- **registrar_sistema, obtener_sistemas, obtener_info**: Métodos de instancia que operan sobre el singleton

### Relaciones
- **Self-containment**: La clase se contiene a sí misma a través del atributo estático _instancia
- **Asociación con SistemaHVAC**: El singleton mantiene una lista de sistemas registrados

### Beneficios en el Sistema HVAC
- Centraliza el registro de todos los sistemas HVAC en un único punto
- Evita duplicación de controles y inconsistencias en los datos
- Permite consultas globales del estado del sistema vía GET /control-central
- Garantiza que todas las partes del sistema trabajen con los mismos datos

---

## 3. STRATEGY

### Propósito del Diagrama
El diagrama UML de Strategy muestra cómo definir una familia de algoritmos, encapsular cada uno y hacerlos intercambiables. En el contexto HVAC, permite cambiar dinámicamente el algoritmo de control de temperatura según el modo deseado.

### Componentes del Diagrama
- **EstrategiaClimatizacion (Abstract Strategy)**: Interfaz que define el método ejecutar()
- **EstrategiaEco, EstrategiaConfort, EstrategiaTurbo (Concrete Strategies)**: Implementaciones concretas con diferentes algoritmos de climatización
- **SistemaClimatizacion (Context)**: Clase que utiliza la estrategia y permite cambiarla dinámicamente

### Relaciones
- **Herencia**: Las estrategias concretas heredan de EstrategiaClimatizacion
- **Composición/Asociación**: SistemaClimatizacion tiene una referencia a EstrategiaClimatizacion
- **Uso**: SistemaClimatizacion llama al método ejecutar() de la estrategia actual

### Beneficios en el Sistema HVAC
- Permite cambiar el modo de operación (ECO, CONFORT, TURBO) sin modificar el código del sistema
- Facilita la agregación de nuevas estrategias (ej: modo nocturno, vacaciones)
- Separa la lógica de control de la implementación específica
- Permite probar cada estrategia de forma aislada

---

## 4. STATE

### Propósito del Diagrama
El diagrama UML de State muestra cómo permitir que un objeto altere su comportamiento cuando su estado interno cambia. En el contexto HVAC, el sistema se comporta diferente según esté apagado, operando o en mantenimiento.

### Componentes del Diagrama
- **EstadoHVAC (Abstract State)**: Interfaz que define el método ejecutar()
- **Apagado, Operando, Mantenimiento (Concrete States)**: Implementaciones concretas con comportamientos específicos
- **SistemaHVAC (Context)**: Clase que mantiene una referencia al estado actual y delega comportamiento

### Relaciones
- **Herencia**: Los estados concretos heredan de EstadoHVAC
- **Composición/Asociación**: SistemaHVAC tiene una referencia a EstadoHVAC
- **Delegación**: SistemaHVAC delega el comportamiento al estado actual

### Beneficios en el Sistema HVAC
- Elimina condicionales complejos para verificar el estado
- Facilita la agregación de nuevos estados (ej: error, standby)
- Cada estado encapsula su propio comportamiento
- Permite transiciones de estado controladas y validadas

### Corrección Implementada
Se corrigió el problema donde el estado siempre devolvía "Apagado". Ahora:
- El estado inicial depende del estado del equipo (encendido/apagado)
- Se puede cambiar dinámicamente vía PUT /habitaciones/{nombre}/estado
- El comportamiento refleja correctamente el estado actual del sistema

---

## 5. OBSERVER

### Propósito del Diagrama
El diagrama UML de Observer muestra cómo definir una dependencia uno-a-muchos entre objetos para que cuando uno cambie de estado, todos sus dependientes sean notificados. En el contexto HVAC, permite notificar a múltiples componentes cuando ocurren eventos.

### Componentes del Diagrama
- **Observador (Abstract Observer)**: Interfaz que define el método actualizar()
- **Pantalla, AppMovil, RegistroSistema (Concrete Observers)**: Implementaciones concretas que reaccionan a eventos
- **GestorEventos (Subject)**: Clase que mantiene la lista de observadores y los notifica

### Relaciones
- **Herencia**: Los observadores concretos heredan de Observador
- **Composición/Asociación**: GestorEventos mantiene una lista de Observador
- **Notificación**: GestorEventos llama a actualizar() en cada observador registrado

### Beneficios en el Sistema HVAC
- Permite notificar simultáneamente a múltiples componentes sin acoplamiento fuerte
- Facilita la agregación de nuevos tipos de observadores (ej: email, SMS)
- Permite configurar diferentes combinaciones de observadores por habitación
- Separa la generación de eventos del manejo de notificaciones

### Integración con la API
- **PUT /habitaciones/{nombre}/observadores**: Configura qué observadores recibirán notificaciones
- **POST /habitaciones/{nombre}/evento**: Envía eventos a todos los observadores configurados

---

## INTEGRACIÓN DE TODOS LOS PATRONES

Los cinco patrones trabajan juntos en el sistema HVAC:

1. **Factory Method**: Crea los equipos HVAC dinámicamente
2. **Singleton**: Centraliza el control de todos los sistemas
3. **Strategy**: Permite cambiar el algoritmo de climatización
4. **State**: Maneja los diferentes estados operacionales
5. **Observer**: Notifica eventos a múltiples componentes

Esta integración proporciona un sistema flexible, extensible y mantenible que puede adaptarse a diferentes necesidades sin modificar su estructura fundamental.

---

## REFERENCIAS

Los diagramas UML originales están disponibles en el archivo `patrones/PATRONES.IPYNB` y pueden visualizarse en:
- [PlantUML Editor](https://editor.plantuml.com/)
- Los enlaces directos en el notebook redirigen a los diagramas renderizados

Para ejecutar las pruebas de validación de todos los patrones:
```bash
python tests_patrones.py
```