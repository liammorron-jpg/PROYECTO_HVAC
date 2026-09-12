# Sistema HVAC con patrones de diseno

Estructura inicial de un sistema HVAC en Python organizado en cinco patrones de diseno.

## Patrones

- `patrones/factory_method.py`: crea equipos HVAC mediante Factory Method.
- `patrones/observer.py`: notifica cambios de estado a paneles y alarmas.
- `patrones/singleton.py`: centraliza la configuracion compartida del sistema.
- `patrones/state.py`: controla los estados encendido y apagado.
- `patrones/strategy.py`: permite cambiar el algoritmo de control de temperatura.

# Sistema de Monitoreo HVAC

Sistema de monitoreo y control HVAC desarrollado en **Python** utilizando **FastAPI** y patrones de diseño de software.

El proyecto permite gestionar habitaciones o zonas, crear diferentes equipos HVAC, controlar su estado y consultar la información del sistema mediante una API REST y un panel web.

## Tecnologías utilizadas

* Python
* FastAPI
* Uvicorn
* HTML
* Programación Orientada a Objetos (POO)
* API REST

## Patrones de diseño

El sistema implementa cinco patrones de diseño:

### 1. Factory Method

Archivo:

`patrones/factory_method.py`

Se encarga de crear diferentes tipos de equipos HVAC sin depender directamente de sus clases concretas.

Equipos disponibles:

* Aire acondicionado
* Calefactor
* Ventilador

### 2. Observer

Archivo:

`patrones/observer.py`

Permite notificar eventos o cambios producidos dentro del sistema HVAC.

Esto facilita que diferentes componentes puedan reaccionar ante cambios sin estar fuertemente acoplados.

### 3. Singleton

Archivo:

`patrones/singleton.py`

Implementa un único `ControlCentralHVAC` encargado de registrar y centralizar los sistemas HVAC existentes.

De esta forma se garantiza que toda la aplicación utilice una misma instancia del control central.

### 4. State

Archivo:

`patrones/state.py`

Controla los diferentes estados de funcionamiento del sistema.

Por ejemplo:

* Encendido
* Apagado

El comportamiento del sistema puede cambiar dependiendo de su estado actual.

### 5. Strategy

Archivo:

`patrones/strategy.py`

Permite utilizar diferentes estrategias de climatización sin modificar la estructura principal del sistema.

El sistema puede cambiar su algoritmo de control de temperatura de manera flexible.

## Estructura del proyecto

```text
PROYECTO_HVAC/
│
├── main.py
├── .gitignore
├── README.md
│
├── API/
│   ├── __init__.py
│   ├── hvac_api.py
│   ├── panel_hvac.html
│   └── logo_hvac.svg
│
├── modelos/
│   ├── __init__.py
│   ├── habitacion.py
│   └── sistema_hvac.py
│
└── patrones/
    ├── __init__.py
    ├── factory_method.py
    ├── observer.py
    ├── singleton.py
    ├── state.py
    └── strategy.py
```

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Entrar al proyecto:

```bash
cd PROYECTO_HVAC
```

Instalar las dependencias:

```bash
pip install fastapi uvicorn
```

## Ejecutar el proyecto

Desde la raíz del proyecto ejecutar:

```bash
python main.py
```

El servidor se iniciará en:

```text
http://127.0.0.1:8001
```

## Accesos

Una vez iniciado el servidor estarán disponibles los siguientes servicios:

### API

```text
http://127.0.0.1:8001
```

### Panel HVAC

```text
http://127.0.0.1:8001/panel
```

### Swagger

FastAPI genera automáticamente la documentación interactiva de la API mediante Swagger UI:

```text
http://127.0.0.1:8001/docs
```

Desde Swagger es posible consultar y probar directamente los endpoints disponibles.

## Endpoints principales

### Consultar o registrar una habitación

```http
GET /habitaciones/{nombre}
```

Permite consultar una habitación. Si todavía no existe, el sistema puede crearla con su configuración HVAC.

### Listar habitaciones

```http
GET /habitaciones
```

Devuelve todas las habitaciones o zonas registradas.

### Cambiar equipo

```http
PUT /habitaciones/{nombre}/equipo
```

Permite cambiar el tipo de equipo HVAC asociado a una habitación.

### Encender o apagar equipo

```http
PUT /habitaciones/{nombre}/equipo/estado
```

Permite modificar el estado del equipo HVAC.

### Control central

```http
GET /control-central
```

Permite consultar la información almacenada por el control central implementado mediante Singleton.

## Objetivo del proyecto

El objetivo es demostrar la aplicación práctica de patrones de diseño dentro de un sistema HVAC, manteniendo una arquitectura modular, organizada y extensible.

La implementación de **Factory Method, Observer, Singleton, State y Strategy** permite separar responsabilidades y facilitar la incorporación de nuevos equipos, estados, estrategias y funcionalidades sin modificar innecesariamente los componentes existentes.

