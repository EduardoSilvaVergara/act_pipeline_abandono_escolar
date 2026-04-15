import pandas as pd
import logging
import os
from datetime import datetime

# Configuración de rutas
INPUT_FILE = "data/abandono_escolar_dataset.csv"
OUTPUT_FILE = "output/processed_data.csv"
LOG_FILE = "logs/ingestion.log"

# Crear carpetas si no existen
os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Configuración de logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ingest_data():
    logging.info("Inicio del proceso de ingesta")

    try:
        # Leer CSV
        df = pd.read_csv(INPUT_FILE)
        logging.info(f"Archivo leído correctamente. Registros encontrados: {len(df)}")

        # Transformación básica (ejemplo)
        df.columns = [col.strip().lower() for col in df.columns]

        # Eliminar duplicados
        df = df.drop_duplicates()

        # Agregar timestamp de procesamiento
        df["processed_at"] = datetime.now()

        # Guardar datos procesados
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Datos procesados y guardados correctamente en {OUTPUT_FILE}")
        logging.info(f"Total de registros procesados: {len(df)}")

    except Exception as e:
        logging.error(f"Error en el proceso de ingesta: {str(e)}")
        raise

    logging.info("Fin del proceso de ingesta")


if __name__ == "__main__":
    ingest_data()