
import logging

from cliente import Cliente, ejecutar_ejemplo
from reserva import ErrorReserva, EstadoReservaError, Reserva
from servicio import AlquilerEquipo, Asesoria, ReservaSala

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)



if __name__ == "__main__":
    try:
        Cliente("C002", "Eva", "correo-invalido", "3001234567")
    except ValueError as error:
        logging.exception("Prueba de correo inválido")
        print(f"Prueba de correo inválido: {error}")

    try:
        Cliente("C003", "Luis", "luis@example.com", "123")
    except ValueError as error:
        logging.exception("Prueba de teléfono inválido")
        print(f"Prueba de teléfono inválido: {error}")

    try:
        Cliente("", "Eva", "eva@example.com", "3001234567")
    except ValueError as error:
        logging.exception("Prueba de identificador inválido")
        print(f"Prueba de identificador inválido: {error}")

    try:
        Cliente("C004", "", "maria@example.com", "3001234567")
    except ValueError as error:
        logging.exception("Prueba de nombre inválido")
        print(f"Prueba de nombre inválido: {error}")

    try:
        ReservaSala("S004", "Sala inválida", 50000, 0)
    except ValueError as error:
        logging.exception("Prueba de servicio inválido")
        print(f"Prueba de servicio inválido: {error}")

    try:
        Asesoria("S005", "Asesoría sin tema", 80000, "", "Luis")
    except ValueError as error:
        logging.exception("Prueba de asesoria inválida")
        print(f"Prueba de asesoría inválida: {error}") 

    cliente_prueba = Cliente(
        "C005", "Carlos", "carlos@example.com", "3001234567"
    )
    sala_prueba = ReservaSala("S006", "Sala de prueba", 50000, 10)

    try:
        Reserva("R004", cliente_prueba, sala_prueba, 0)
    except (ValueError, TypeError) as error:
        logging.exception("Prueba de reserva inválida")
        print(f"Prueba de reserva inválida: {error}")

        cliente_prueba = Cliente(
        "C005", "Carlos", "carlos@example.com", "3001234567"
    )
    sala_prueba = ReservaSala("S006", "Sala de prueba", 50000, 10)


    cliente_estado = Cliente(
        "C006", "Laura", "laura@example.com", "3001234567"
    )
    sala_estado = ReservaSala("S007", "Sala de prueba", 50000, 10)
    reserva_estado = Reserva(
        "R005", cliente_estado, sala_estado, 1
    )

    reserva_estado.confirmar()

    try:
        reserva_estado.confirmar()
    except EstadoReservaError as error:
        logging.exception("Prueba de confirmación repetida")
        print(f"Prueba de excepción personalizada: {error}")

    cliente_equipo = Cliente(
        "C007", "Sofía", "sofia@example.com", "3001234567"
    )
    equipo_agotado = AlquilerEquipo(
        "S008", "Proyector", 30000, 0
    )
    reserva_agotada = Reserva(
        "R006", cliente_equipo, equipo_agotado, 1, unidades=1
    )

    try:
        reserva_agotada.confirmar()
    except ErrorReserva as error:
        logging.exception("Prueba de servicio sin unidades")
        print(f"Prueba de error encadenado: {error}")


    ejecutar_ejemplo()

