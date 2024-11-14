import os
import psycopg2
from glob import glob
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configuración de la base de datos desde .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
CSV_FOLDER = os.getenv("CSV_FOLDER")

# Conexión a la base de datos
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Lista de archivos CSV
csv_files = glob(os.path.join(CSV_FOLDER, "*.csv"))

# Importar cada archivo
for csv_file in csv_files:
    # Determinar la tabla según el nombre del archivo (asume formato nombre_tabla.csv)
    table_name = os.path.basename(csv_file).split('_')[0]  # Ejemplo: homicidios_2023.csv -> homicidios
    print(f"Importando {csv_file} a la tabla {table_name}...")
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            cursor.copy_expert(f"""
                COPY {table_name} (entidad, municipio, num_muertos, hombres, mujeres, no_identificado, fuente, fecha)
                FROM STDIN
                WITH CSV HEADER DELIMITER ',';
            """, f)
        conn.commit()
        print(f"{csv_file} importado con éxito.")
    except Exception as e:
        conn.rollback()
        print(f"Error al importar {csv_file}: {e}")

# Cerrar conexión
cursor.close()
conn.close()
