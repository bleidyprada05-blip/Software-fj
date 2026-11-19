#Configuración del registro de eventos y errores de Software FJ
import logging

ARCHIVO_LOG = "software_fj.log"

#Configura el archivo de logs
def configurar_logs():
     logging.basicConfig(
        filename=ARCHIVO_LOG,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )
