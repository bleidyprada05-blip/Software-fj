
from datetime import datetime
import logging

from cliente import Cliente
from servicio import AlquilerEquipo, Servicio
from excepciones import ErrorReserva, EstadoReservaError

logger = logging.getLogger(__name__)


class Reserva:
    """Conecta un cliente con un servicio y administra su reserva."""

    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion,
        unidades=1,
        impuesto=0,
        descuento=0,
    ):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador de la reserva no puede estar vacío.")
        if not all(
            hasattr(cliente, atributo)
            for atributo in ("identificador", "nombre", "correo", "telefono")
        ):
            raise TypeError("El cliente debe ser una instancia compatible con Cliente.")
        if not isinstance(servicio, Servicio):
            raise TypeError("El servicio debe ser una instancia de Servicio.")
        Servicio._validar_cantidad(duracion)
        if isinstance(unidades, bool) or not isinstance(unidades, int):
            raise TypeError("La cantidad de unidades debe ser un número entero.")
        if unidades <= 0:
            raise ValueError("La cantidad de unidades debe ser mayor que cero.")
        if not isinstance(servicio, AlquilerEquipo) and unidades != 1:
            raise ValueError(
                "El parámetro unidades solo aplica al alquiler de equipos."
            )

        self._identificador = identificador.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._unidades = unidades
        self._impuesto = impuesto
        self._descuento = descuento
        self._estado = self.PENDIENTE
        self._costo = None
        self._fecha_creacion = datetime.now()
        self._fecha_confirmacion = None
        self._fecha_cancelacion = None
        logger.info(
            "Reserva %s creada para el cliente %s.",
            self.identificador,
            self.cliente.identificador,
        )

    @property
    def identificador(self):
        """Devuelve el identificador único de la reserva."""
        return self._identificador

    @property
    def cliente(self):
        """Devuelve el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Devuelve el servicio asociado a la reserva."""
        return self._servicio

    @property
    def duracion(self):
        """Devuelve la duración de la reserva en unidades del servicio."""
        return self._duracion

    @property
    def unidades(self):
        """Devuelve la cantidad de unidades solicitadas para el servicio."""
        return self._unidades

    @property
    def estado(self):
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def costo(self):
        """Devuelve el costo calculado de la reserva, si ya fue confirmado."""
        return self._costo

    @property
    def fecha_creacion(self):
        """Devuelve la fecha en que se creó la reserva."""
        return self._fecha_creacion

    @property
    def fecha_confirmacion(self):
        """Devuelve la fecha en que la reserva fue confirmada."""
        return self._fecha_confirmacion

    @property
    def fecha_cancelacion(self):
        """Devuelve la fecha en que la reserva fue cancelada."""
        return self._fecha_cancelacion

    def _calcular_costo(self):
        argumentos = {
            "cantidad": self.duracion,
            "impuesto": self._impuesto,
            "descuento": self._descuento,
        }
        if isinstance(self.servicio, AlquilerEquipo):
            argumentos["unidades"] = self.unidades
        return self.servicio.calcular_costo(**argumentos)

    def confirmar(self):
        """Calcula el costo y confirma una reserva pendiente."""
        if self.estado != self.PENDIENTE:
            error = EstadoReservaError(
                f"No se puede confirmar una reserva en estado '{self.estado}'."
            )
            logger.error(
                "Error al confirmar la reserva %s: %s", self.identificador, error
            )
            raise error
        try:
            costo = self._calcular_costo()
            if isinstance(self.servicio, AlquilerEquipo):
                self.servicio.reservar_unidades(self.unidades)
        except Exception as error:
            logger.exception(
                "Falló el cálculo al confirmar la reserva %s.", self.identificador
            )
            raise ErrorReserva(
                f"No fue posible confirmar la reserva {self.identificador}."
            ) from error

        self._costo = costo
        self._estado = self.CONFIRMADA
        self._fecha_confirmacion = datetime.now()
        logger.info(
            "Reserva %s confirmada. Costo: %.2f.", self.identificador, self.costo
        )
        return self.costo

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""
        if self.estado == self.CANCELADA:
            error = EstadoReservaError("La reserva ya se encuentra cancelada.")
            logger.error(
                "Error al cancelar la reserva %s: %s", self.identificador, error
            )
            raise error
        if self.estado == self.CONFIRMADA and isinstance(
            self.servicio, AlquilerEquipo
        ):
            self.servicio.liberar_unidades(self.unidades)
        self._estado = self.CANCELADA
        self._fecha_cancelacion = datetime.now()
        logger.info("Reserva %s cancelada.", self.identificador)
        return self.estado
    

    def procesar(self):
        """Procesa la reserva y registra el resultado del intento."""
        try:
            if self.estado == self.PENDIENTE:
                self.confirmar()
            elif self.estado == self.CANCELADA:
                raise EstadoReservaError(
                    "No se puede procesar una reserva cancelada."
                )

        except ErrorReserva:
            logger.exception(
                "No se pudo procesar la reserva %s.",
                self.identificador
            )
            raise

        else:
            return self.mostrar_informacion()

        finally:
            logger.info(
                "Finalizó el intento de procesar la reserva %s.",
                self.identificador
            )


    
    def mostrar_informacion(self):
        """Devuelve los datos principales de la reserva."""
        costo = f"{self.costo:.2f}" if self.costo is not None else "pendiente"
        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} ({self.cliente.identificador}) | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Unidades: {self.unidades} | Estado: {self.estado} | Costo: {costo}"
        )