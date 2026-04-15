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
    logging.info("=== INICIO DEL PIPELINE ===")

    try:
        # 📌 Validar existencia del archivo
        if not os.path.exists(INPUT_FILE):
            logging.error("El archivo de entrada no existe")
            raise FileNotFoundError(f"No se encontró {INPUT_FILE}")

        # 📥 Leer CSV
        df = pd.read_csv(INPUT_FILE)
        logging.info(f"Archivo leído correctamente. Registros: {len(df)}")

        # 🧹 Normalizar columnas
        df.columns = [col.strip().lower() for col in df.columns]

        # 📊 Información básica del dataset
        logging.info(f"Columnas detectadas: {list(df.columns)}")

        # ❌ Valores nulos
        nulls = df.isnull().sum().sum()
        logging.info(f"Valores nulos totales: {nulls}")

        # 🔁 Eliminar duplicados
        before = len(df)
        df = df.drop_duplicates()
        logging.info(f"Duplicados eliminados: {before - len(df)}")

        # 🎯 Feature engineering: riesgo de abandono
        df["riesgo_abandono"] = df["abandono"].apply(
            lambda x: "alto riesgo" if x == 1 else "bajo riesgo"
        )

        # ⏱ Timestamp de procesamiento
        df["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 📤 Guardar output
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Datos guardados en: {OUTPUT_FILE}")

        # 📈 Métricas finales
        logging.info(f"Registros finales: {len(df)}")
        logging.info("=== PIPELINE FINALIZADO EXITOSAMENTE ===")

    except Exception as e:
        logging.error(f"ERROR EN PIPELINE: {str(e)}")
        raise


if __name__ == "__main__":
    ingest_data()