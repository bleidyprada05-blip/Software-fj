#Menú principal del sistema de Software FJ
import logging

from cliente import Cliente
from excepciones import ErrorFJ, ErrorReserva, EstadoReservaError
from logger import configurar_logs
from reserva import Reserva
from servicio import AlquilerEquipo, Asesoria, ReservaSala

logger = logging.getLogger(__name__)

ERRORES = (ErrorFJ, ValueError, TypeError)

clientes = {}
reservas = {}
servicios = {
    servicio.identificador: servicio
    for servicio in (
        ReservaSala("S001", "Sala Norte", 50000, 12, ["Proyector", "Pizarra"]),
        AlquilerEquipo("S002", "Portátil", 30000, 5),
        Asesoria("S003", "Asesoría técnica", 80000, "desarrollo", "Luis Gómez"),
    )
}

#Muestra el error al usuario y lo deja registrado en el log
def mostrar_error(error):
    logger.warning("Operación rechazada: %s", error)
    print(f"Error: {error}")
    if error.__cause__:
        print(f"Motivo: {error.__cause__}")

#Lee un número; si se deja vacío y hay valor por defecto, lo usa
def leer_numero(texto, tipo=float, defecto=None):    
    valor = input(texto).strip()
    if not valor and defecto is not None:
        return defecto
    return tipo(valor)


#RegistraClientes
def registrar_cliente():
    try:
        cliente = Cliente(
            input("ID: "), input("Nombre: "), input("Correo: "), input("Teléfono: ")
        )
        clientes[cliente.identificador] = cliente
        print("Cliente registrado.")
    except ERRORES as error:
        mostrar_error(error)


def listar_clientes():
    if not clientes:
        print("No hay clientes registrados.")
    for cliente in clientes.values():
        print(cliente.mostrar_informacion())


#VerificaServicios
def ver_servicios():
    for servicio in servicios.values():
        print(f"[{servicio.identificador}] {servicio.describir()}")


#CreaReserva
def crear_reserva():
    try:
        cliente = clientes.get(input("ID del cliente: ").strip())
        servicio = servicios.get(input("ID del servicio: ").strip().upper())
        if cliente is None or servicio is None:
            print("Cliente o servicio no encontrado.")
            return
        duracion = leer_numero("Duración (horas o días): ")
        unidades = 1
        if isinstance(servicio, AlquilerEquipo):
            unidades = leer_numero("Unidades a alquilar: ", int)
        impuesto = leer_numero("Impuesto % [0]: ", float, 0)
        descuento = leer_numero("Descuento % [0]: ", float, 0)

        identificador = f"R{len(reservas) + 1:03d}"
        reserva = Reserva(
            identificador, cliente, servicio, duracion, unidades, impuesto, descuento
        )
        reservas[identificador] = reserva
        print(reserva.mostrar_informacion())
    except ERRORES as error:
        mostrar_error(error)


def gestionar_reserva(accion):
    reserva = reservas.get(input("ID de la reserva: ").strip().upper())
    if reserva is None:
        print("Reserva no encontrada.")
        return
    try:
        if accion == "confirmar":
            print(f"Reserva confirmada. Costo: {reserva.confirmar():.2f}")
        else:
            reserva.cancelar()
            print("Reserva cancelada.")
    except ERRORES as error:
        mostrar_error(error)


def listar_reservas():
    if not reservas:
        print("No hay reservas registradas.")
    for reserva in reservas.values():
        print(reserva.mostrar_informacion())

#Pruebas
def probar(descripcion, accion, errores=ERRORES):
    """Ejecuta una acción que debe fallar y registra el error esperado."""
    try:
        accion()
    except errores as error:
        logger.exception("Prueba de %s", descripcion)
        print(f"Prueba de {descripcion}: {error}")
    else:
        print(f"Prueba de {descripcion}: no lanzó ningún error.")


def ejecutar_pruebas():
    probar("correo inválido", lambda: Cliente("C002", "Eva", "correo-invalido", "3001234567"))
    probar("teléfono inválido", lambda: Cliente("C003", "Luis", "luis@example.com", "123"))
    probar("identificador inválido", lambda: Cliente("", "Eva", "eva@example.com", "3001234567"))
    probar("nombre inválido", lambda: Cliente("C004", "", "maria@example.com", "3001234567"))
    probar("servicio inválido", lambda: ReservaSala("S004", "Sala inválida", 50000, 0))
    probar("asesoría inválida", lambda: Asesoria("S005", "Asesoría sin tema", 80000, "", "Luis"))

    cliente = Cliente("C005", "Carlos", "carlos@example.com", "3001234567")
    sala = ReservaSala("S006", "Sala de prueba", 50000, 10)
    probar("reserva inválida", lambda: Reserva("R004", cliente, sala, 0))

    reserva = Reserva("R005", cliente, sala, 1)
    reserva.confirmar()
    probar("confirmación repetida", reserva.confirmar, (EstadoReservaError,))

    equipo = AlquilerEquipo("S008", "Proyector", 30000, 0)
    agotada = Reserva("R006", cliente, equipo, 1, unidades=1)
    probar("servicio sin unidades", agotada.confirmar, (ErrorReserva,))


def ejecutar_ejemplo():
    cliente = Cliente("C001", "Ana Pérez", "ana@example.com", "3001234567")
    ejemplos = [
        ReservaSala("S001", "Sala Norte", 50000, 12, ["Proyector", "Pizarra"]),
        AlquilerEquipo("S002", "Portátil", 30000, 5),
        Asesoria("S003", "Asesoría técnica", 80000, "desarrollo", "Luis Gómez"),
    ]
    reservas_ejemplo = [
        Reserva("R001", cliente, ejemplos[0], 2, impuesto=19),
        Reserva("R002", cliente, ejemplos[1], 3, unidades=2, descuento=10),
        Reserva("R003", cliente, ejemplos[2], 1.5),
    ]
    print(cliente.mostrar_informacion())
    for servicio, reserva in zip(ejemplos, reservas_ejemplo):
        print(servicio.describir())
        print(reserva.procesar())
        print()


#MenuPrincipal
def menu():
    acciones = {
        "1": registrar_cliente,
        "2": listar_clientes,
        "3": ver_servicios,
        "4": crear_reserva,
        "5": lambda: gestionar_reserva("confirmar"),
        "6": lambda: gestionar_reserva("cancelar"),
        "7": listar_reservas,
        "8": ejecutar_pruebas,
        "9": ejecutar_ejemplo,
    }
    while True:
        print("\n--- Software FJ ---")
        print("1). Registrar cliente")
        print("2). Listar clientes")
        print("3). Ver servicios")
        print("4). Crear reserva")
        print("5). Confirmar reserva")
        print("6). Cancelar reserva")
        print("7). Listar reservas")
        print("8). Ejecutar pruebas de validación")
        print("9). Ejecutar ejemplo completo")
        print("0). Salir")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("Hasta pronto.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida.")
            continue
        try:
            accion()
        except ERRORES as error:
            mostrar_error(error)


if __name__ == "__main__":
    configurar_logs()
    menu()
