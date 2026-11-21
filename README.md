# Software FJ

Sistema en Python con programación orientada a objetos para gestionar clientes, servicios y reservas. No utiliza bases de datos; los datos se conservan en memoria mientras el programa está abierto.

## Requisitos

- Python 3.9 o superior.
- No requiere instalar librerías externas.

## Ejecución

Desde la carpeta del proyecto, ejecuta:

```bash
python main.py
```

El programa abrirá el menú principal.

## Opciones del menú

| Opción | Acción |
|---|---|
| 1 | Registrar cliente |
| 2 | Listar clientes |
| 3 | Ver servicios disponibles |
| 4 | Crear reserva |
| 5 | Confirmar reserva y calcular el costo |
| 6 | Cancelar reserva |
| 7 | Listar reservas |
| 8 | Ejecutar pruebas de validación |
| 9 | Ejecutar ejemplo completo |
| 0 | Salir |

## Archivos del proyecto

| Archivo | Contenido |
|---|---|
| `cliente.py` | Clase `Cliente` y validación de sus datos |
| `servicio.py` | Clase abstracta `Servicio` y servicios especializados |
| `reserva.py` | Clase `Reserva`, confirmación y cancelación |
| `excepciones.py` | Excepciones personalizadas |
| `logger.py` | Configuración del registro de eventos y errores |
| `Menu.py` | Opciones y operaciones del menú |
| `main.py` | Inicio de la aplicación |

## Servicios

- **Reserva de sala:** tarifa por hora.
- **Alquiler de equipos:** tarifa por día y unidad, con control de inventario.
- **Asesoría:** tarifa por hora, con especialidad y asesor.

## Registro de eventos

Los eventos y errores se guardan en `software_fj.log`. Este archivo se crea al ejecutar el programa. Los clientes y reservas permanecen en memoria y desaparecen al cerrar la aplicación.