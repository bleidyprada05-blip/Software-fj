"""Sistema integrado de clientes, servicios y reservas de Software FJ.

Contiene las clases Cliente, Servicio, ReservaSala, AlquilerEquipo, Asesoria
y Reserva. No utiliza bases de datos; conserva los datos en objetos.
"""
from abc import ABC, abstractmethod
from datetime import datetime
import logging
from servicio import Servicio, ReservaSala, AlquilerEquipo, Asesoria

logger = logging.getLogger(__name__)

class Cliente:
    """Representa a un cliente de Software FJ."""

    def __init__(self, identificador, nombre, correo, telefono):

        if not identificador.strip():
            raise ValueError("El identificador no puede estar vacío.")

        
        self.identificador = identificador.strip()
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono.strip()

    #Permite consultar el telefono guardado

    @property
    def telefono(self):
        return self._telefono


    # Valida el telefono antes de guardarlo
    @telefono.setter
    def telefono(self, valor):
        if not valor.isdigit() or not 7 <= len(valor) <= 15:
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")

        self._telefono = valor

    #Permite consultar el nombre del cliente

    @property
    def nombre(self):
        return self._nombre

    # Valida el nombre antes de guardarlo

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")

        self._nombre = valor.strip()

    # Permite consultar el correo guardado
    @property
    def correo(self):
        return self._correo


    # Valida el correo antes de guardarlo
    @correo.setter
    def correo(self, valor):
        # Comprueba de forma básica que el correo tenga @ y un punto.
        if not isinstance(valor, str):
            raise ValueError("El correo debe ser texto.")

        partes = valor.strip().split("@")

        if len(partes) != 2:
            raise ValueError("El correo debe tener un solo símbolo @.")

        usuario, dominio = partes

        if not usuario or "." not in dominio:
            raise ValueError("El correo debe tener un usuario y un dominio válido.")

        nombre_dominio, separador, extension = dominio.rpartition(".")

        if not nombre_dominio or len(extension) < 2:
            raise ValueError("El correo debe terminar con una extensión válida, como .com.")

        self._correo = valor.strip().lower()

    def mostrar_informacion(self):
        """Devuelve los datos del cliente en un texto."""
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )

        




def ejecutar_ejemplo():
    """Ejecuta un ejemplo válido de reserva para los tres servicios."""
    from reserva import Reserva
    
    logging.basicConfig(
        filename="software_fj.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )

    cliente = Cliente("C001", "Ana Pérez", "ana@example.com", "3001234567")
    servicios = [
        ReservaSala("S001", "Sala Norte", 50000, 12, ["Proyector", "Pizarra"]),
        AlquilerEquipo("S002", "Portátil", 30000, 5),
        Asesoria("S003", "Asesoría técnica", 80000, "desarrollo", "Luis Gómez"),
    ]
    reservas = [
        Reserva("R001", cliente, servicios[0], 2, impuesto=19),
        Reserva("R002", cliente, servicios[1], 3, unidades=2, descuento=10),
        Reserva("R003", cliente, servicios[2], 1.5),
    ]

    print(cliente.mostrar_informacion())
    for servicio, reserva in zip(servicios, reservas):
        print(servicio.describir())
        print(reserva.procesar())
        print()

if __name__== "__main__":
    ejecutar_ejemplo()
