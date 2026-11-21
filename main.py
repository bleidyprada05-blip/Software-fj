"""Punto de entrada del sistema Software FJ."""

from Menu import menu
from logger import configurar_logs


if __name__ == "__main__":
    configurar_logs()
    menu()