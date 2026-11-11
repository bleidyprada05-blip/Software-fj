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