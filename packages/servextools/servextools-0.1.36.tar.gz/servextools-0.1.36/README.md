# ServexTools
[![PyPI version](https://badge.fury.io/py/servextools.svg)](https://pypi.org/project/servextools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
Herramientas avanzadas para sistemas empresariales Python/Flask

---

## Descripción General
ServexTools es una colección de utilidades y componentes para acelerar el desarrollo de sistemas empresariales, especialmente aquellos basados en Flask y MongoDB. Incluye funciones para manejo de base de datos, generación de tablas HTML, manejo de sesiones, replicación de datos, logs avanzados, y más.

### Características principales
- **Integración con Flask y MongoDB**: CRUD, replicación, manejo de sesiones y seguridad.
- **Generación avanzada de tablas HTML**: Paginación, formateo, totales, marcado condicional y procesamiento eficiente con Polars y Numpy.
- **Utilidades de fecha/hora**: Conversión, formateo y cálculo de diferencias.
- **Logs y monitoreo**: Escritura de logs con rotación automática y soporte para consola y procesos.
- **Operaciones con archivos y directorios**: Manipulación, borrado seguro, compresión/descompresión.
- **Encriptación y seguridad**: JWT, manejo seguro de datos sensibles.
- **Componentes reutilizables**: Manejo de sesiones, tablas, replicación, y más.

---

## Estructura del Proyecto

```
ServexTools/
├── Tools.py           # Utilidades generales (fechas, archivos, formateo, logs, API, etc.)
├── Table.py           # Generación de tablas HTML avanzadas
├── ReplicaDb.py       # Replicación de datos MongoDB
├── EscribirLog.py     # Escritura y rotación de logs
├── GetTime.py         # Utilidades de tiempo y fecha
├── Necesario.py       # Manejo de sesiones y paginación avanzada
├── conexion.py        # Conexión y operaciones con MongoDB/SQLite
├── socket_manager.py  # Manejo de WebSockets con Flask-SocketIO
├── Enumerable.py      # Enumeraciones y constantes
├── TablePV.py         # Tablas para punto de venta
└── __init__.py        # Inicialización del paquete
```

---

## Uso Rápido

### Conexión y operaciones básicas
```python
from ServexTools import Tools

# Ejemplo: Insertar un documento en MongoDB
coleccion, cliente = Tools.Get('usuarios')
doc = {"nombre": "Juan", "edad": 30}
coleccion.insert_one(doc)

# Ejemplo: Obtener fecha formateada
from ServexTools import Tools
fecha = Tools.DateFormat("25/12/2023")
print(fecha)
```

### Generación de tablas HTML
```python
from ServexTools import Table

datos = [
    {"Nombre": "Juan", "Edad": 30},
    {"Nombre": "Ana", "Edad": 25}
]
columnas = ("Nombre", "Edad")
html = Table.CrearTabla(datos, NombreColumnas=columnas)
print(html)
```

---

## Documentación de Componentes

### Tools.py
- Utilidades generales para fechas, archivos, formateo, logs, encriptación y operaciones API.
- Funciones destacadas:
    - `DateFormat`, `DateTimeFormat`, `StrToDate`, `StrToInt`, `FormatoMoneda`
    - `OptenerDatos(request)`: Extrae y normaliza datos de un request Flask
    - `EscribirLog(texto, tipo)`: Escribe logs rotativos
    - `Encriptar(datos, clave)`, `DesEncriptar(datos, clave)`: Seguridad JWT
    - `TiempoEspera(tiempo, IsGevent)`: Espera con interrupción por archivo .kill

### Table.py
- Generador de tablas HTML dinámicas con paginación, formateo y marcado condicional.
- Soporte para grandes volúmenes de datos usando Polars y Numpy.
- Ejemplo de uso en sección anterior.

### ReplicaDb.py
- Replicación automática de operaciones MongoDB entre instancias.
- Clases: `ReplicaCollection`, `ReplicaDB`, `ReplicaCluster`.
- Métodos compatibles con PyMongo: `insert_one`, `update_one`, `delete_one`, etc.

### Necesario.py
- Manejo avanzado de sesiones y paginación de datos en MongoDB.
- Clase `Session` para almacenar grandes volúmenes en la base.

### EscribirLog.py
- Escritura y rotación de logs por tipo (Error, Consola, Procesos, Update).
- Integración con consola y WebSockets.

### conexion.py
- Abstracción para conexión MongoDB y SQLite.
- Procesamiento seguro de inserciones/actualizaciones.

---

## Dependencias
- flask
- pymongo
- pytz
- PyJWT
- httpx
- gevent
- flask-socketio
- tqdm
- polars-lts-cpu
- numpy

---

## Licencia
MIT - Ver archivo [LICENSE](LICENSE)
