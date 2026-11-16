
from abc import ABC, abstractmethod

class Servicio(ABC):
    """Contrato abstracto común para los servicios de Software FJ."""

    def __init__(self, identificador, nombre, precio_base):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador del servicio no puede estar vacío.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del servicio no puede estar vacío.")
        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)):
            raise TypeError("El precio base debe ser numérico.")
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")
        self._identificador = identificador.strip()
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)

    @property
    def identificador(self):
        """Devuelve el identificador único del servicio."""
        return self._identificador

    @property
    def nombre(self):
        """Devuelve el nombre del servicio."""
        return self._nombre

    @property
    def precio_base(self):
        """Devuelve el precio base del servicio."""
        return self._precio_base

    @staticmethod
    def _validar_cantidad(cantidad):
        """Valida que la cantidad sea mayor que cero."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
            raise TypeError("La cantidad debe ser un número.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

    @staticmethod
    def _aplicar_ajustes(subtotal, impuesto=0, descuento=0):
        """Aplica impuesto y descuento sobre un subtotal dado."""
        for etiqueta, porcentaje in (
            ("impuesto", impuesto),
            ("descuento", descuento),
        ):
            if isinstance(porcentaje, bool) or not isinstance(
                porcentaje, (int, float)
            ):
                raise TypeError(f"El {etiqueta} debe ser numérico.")
            if not 0 <= porcentaje <= 100:
                raise ValueError(f"El {etiqueta} debe estar entre 0 y 100.")
        return round(subtotal * (1 - descuento / 100) * (1 + impuesto / 100), 2)

    @abstractmethod
    def validar_parametros(self):
        """Valida los datos propios del servicio concreto."""

    @abstractmethod
    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        """Calcula el costo para la cantidad indicada."""

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible del servicio."""
class ReservaSala(Servicio):
    """Reserva de sala; su precio base se cobra por hora."""

    def __init__(self, identificador, nombre, precio_base, capacidad, recursos=None):
        super().__init__(identificador, nombre, precio_base)
        self.capacidad = capacidad
        self.recursos = list(recursos) if recursos is not None else []
        self.validar_parametros()

    def validar_parametros(self):
        if isinstance(self.capacidad, bool) or not isinstance(self.capacidad, int):
            raise TypeError("La capacidad debe ser un número entero.")
        if self.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")
        if not all(
            isinstance(recurso, str) and recurso.strip()
            for recurso in self.recursos
        ):
            raise ValueError("Cada recurso de la sala debe tener un nombre válido.")
        return True

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        self.validar_parametros()
        self._validar_cantidad(cantidad)
        subtotal = self.precio_base * cantidad
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        recursos = ", ".join(self.recursos) or "sin recursos adicionales"
        return (
            f"{self.nombre} (reserva de sala): capacidad para {self.capacidad} "
            f"personas; {recursos}. Tarifa por hora: {self.precio_base:.2f}."
        )


class AlquilerEquipo(Servicio):
    """Alquiler de equipo; tarifa por día y por unidad."""

    def __init__(self, identificador, nombre, precio_base, unidades_disponibles):
        super().__init__(identificador, nombre, precio_base)
        self._unidades_disponibles = unidades_disponibles
        self._unidades_totales = unidades_disponibles
        self.validar_parametros()

    @property
    def unidades_disponibles(self):
        """Número de unidades de equipo actualmente disponibles para alquilar."""
        return self._unidades_disponibles

    def validar_parametros(self):
        if isinstance(self.unidades_disponibles, bool) or not isinstance(
            self.unidades_disponibles, int
        ):
            raise TypeError("Las unidades disponibles deben ser un número entero.")
        if self.unidades_disponibles < 0:
            raise ValueError("Las unidades disponibles no pueden ser negativas.")
        return True

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0, unidades=1):
        self.validar_parametros()
        self._validar_cantidad(cantidad)
        if isinstance(unidades, bool) or not isinstance(unidades, int):
            raise TypeError("La cantidad de equipos debe ser un número entero.")
        if unidades <= 0:
            raise ValueError("Debe alquilarse al menos una unidad de equipo.")
        if unidades > self.unidades_disponibles:
            raise ValueError("No hay suficientes unidades de equipo disponibles.")
        subtotal = self.precio_base * cantidad * unidades
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def reservar_unidades(self, unidades):
        """Aparta unidades al confirmar una reserva de equipo."""
        if isinstance(unidades, bool) or not isinstance(unidades, int):
            raise TypeError("La cantidad de equipos debe ser un número entero.")
        if unidades <= 0 or unidades > self.unidades_disponibles:
            raise ValueError("No hay suficientes unidades de equipo disponibles.")
        self._unidades_disponibles -= unidades

    def liberar_unidades(self, unidades):
        """Devuelve al inventario las unidades de una reserva cancelada."""
        if isinstance(unidades, bool) or not isinstance(unidades, int):
            raise TypeError("La cantidad de equipos debe ser un número entero.")
        if unidades <= 0:
            raise ValueError("La cantidad de unidades debe ser mayor que cero.")
        if self.unidades_disponibles + unidades > self._unidades_totales:
            raise ValueError("La devolución supera el inventario total del equipo.")
        self._unidades_disponibles += unidades

    def describir(self):
        return (
            f"{self.nombre} (alquiler de equipo): "
            f"{self.unidades_disponibles} unidades disponibles; "
            f"tarifa por día y unidad: {self.precio_base:.2f}."
        )


class Asesoria(Servicio):
    """Asesoría especializada; su precio base se cobra por hora."""

    def __init__(self, identificador, nombre, precio_base, especialidad, asesor):
        super().__init__(identificador, nombre, precio_base)
        self.especialidad = especialidad
        self.asesor = asesor
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.especialidad, str) or not self.especialidad.strip():
            raise ValueError("La especialidad no puede estar vacía.")
        if not isinstance(self.asesor, str) or not self.asesor.strip():
            raise ValueError("El nombre del asesor no puede estar vacío.")
        return True

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        self.validar_parametros()
        self._validar_cantidad(cantidad)
        subtotal = self.precio_base * cantidad
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"{self.nombre} (asesoría en {self.especialidad.strip()}) con "
            f"{self.asesor.strip()}; tarifa por hora: {self.precio_base:.2f}."
        )