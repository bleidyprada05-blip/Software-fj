from cliente import Cliente

try:
    cliente1 = Cliente(
        "CC-001",
        "Ana Pérez",
        "ana@exame.com",
        "3001234567"
    )

    print(cliente1.mostrar_informacion())

except ValueError as error:
    print(f"No se pudo registrar el cliente: {error}")