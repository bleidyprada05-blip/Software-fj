"""Excepciones personalizadas del sistema Software FJ."""


class ErrorFJ(Exception):
    """Excepción base para los errores controlados del sistema."""


class ClienteInvalidoError(ErrorFJ):
    """Datos inválidos de un cliente."""


class ServicioInvalidoError(ErrorFJ):
    """Datos inválidos de un servicio."""


class ServicioNoDisponibleError(ErrorFJ):
    """El servicio o recurso solicitado no está disponible."""


class ReservaInvalidaError(ErrorFJ):
    """Datos inválidos de una reserva."""


class ErrorReserva(ReservaInvalidaError):
    """Error ocurrido durante una operación de reserva."""


class EstadoReservaError(ErrorReserva):
    """Operación no permitida según el estado de la reserva."""