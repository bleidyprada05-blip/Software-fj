"""Sistema integrado de clientes, servicios y reservas de Software FJ.

Contiene las clases Cliente, Servicio, ReservaSala, AlquilerEquipo, Asesoria
y Reserva. No utiliza bases de datos; conserva los datos en objetos.
"""

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
        if "@" not in valor or "." not in valor:
            raise ValueError("El correo debe tener un formato válido.")

        self._correo = valor.strip()

    def mostrar_informacion(self):
        """Devuelve los datos del cliente en un texto."""
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )

        
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


class ErrorReserva(Exception):
    """Error base para las operaciones de reserva."""


class EstadoReservaError(ErrorReserva):
    """Error por intentar una operación no permitida en el estado actual."""


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
        """Confirma si está pendiente y devuelve el resumen de la reserva."""
        try:
            if self.estado == self.PENDIENTE:
                self.confirmar()
            elif self.estado == self.CANCELADA:
                raise EstadoReservaError("No se puede procesar una reserva cancelada.")
            return self.mostrar_informacion()
        except ErrorReserva:
            logger.exception("No se pudo procesar la reserva %s.", self.identificador)
            raise

    def mostrar_informacion(self):
        """Devuelve los datos principales de la reserva."""
        costo = f"{self.costo:.2f}" if self.costo is not None else "pendiente"
        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} ({self.cliente.identificador}) | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Unidades: {self.unidades} | Estado: {self.estado} | Costo: {costo}"
        )


    def ejecutar_ejemplo():
    """Ejecuta un ejemplo válido de reserva para los tres servicios."""
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
