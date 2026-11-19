# Software-fj

Sistema en Python con Programación Orientada a Objetos para gestionar
clientes, servicios y reservas de Software FJ. No usa bases de datos: los
datos se conservan en objetos mientras el programa está abierto.

#Requisitos

- Python 3.9 o superior
- No necesita instalar librerías externas

#Ejecucipm

bash
git clone https://github.com/bleidyprada05-blip/Software-fj.git
cd Software-fj
python main.py


#Opciones del menú

| Opción |
| 1 | Registrar cliente (con validaciones) |
| 2 | Listar clientes |
| 3 | Ver servicios disponibles |
| 4 | Crear reserva |
| 5 | Confirmar reserva (calcula el costo) |
| 6 | Cancelar reserva |
| 7 | Listar reservas |
| 8 | Ejecutar pruebas de validación (errores esperados) |
| 9 | Ejecutar ejemplo completo |
| 0 | Salir |

#Estructura

| Archivo | Contenido |
|---------|-----------|
| `cliente.py` | Clase `Cliente` con sus datos y validaciones |
| `servicio.py` | Clase abstracta `Servicio`, `ReservaSala`, `AlquilerEquipo` y `Asesoria` |
| `reserva.py` | Clase `Reserva`: conecta cliente y servicio, confirma o cancela |
| `excepciones.py` | Excepciones personalizadas |
| `logger.py` | Configuración del registro de eventos y errores |
| `main.py` | Menú principal e integración |

#Servicios

**Reserva de sala:** tarifa por hora.
**Alquiler de equipos:** tarifa por día y por unidad, con control de inventario.
**Asesoría:** tarifa por hora, con especialidad y asesor.

#Registro de eventos

Los eventos y errores se guardan en `software_fj.log` (se crea al ejecutar
el programa). Ejemplo:

2026-11-19 10:30:00 | INFO | Cliente creado: C001
2026-11-19 10:31:12 | ERROR | No se pudo crear el cliente: El teléfono debe tener entre 7 y 15 dígitos.

