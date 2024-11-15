# llenarbd.py
import os
import psycopg2
from glob import glob
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
CSV_FOLDER = os.getenv("CSV_FOLDER")

def llenar_base_de_datos():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    csv_files = glob(os.path.join(CSV_FOLDER, "*.csv"))

    for csv_file in csv_files:
        table_name = os.path.basename(csv_file).split('_')[0]
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

    cursor.close()
    conn.close()

if __name__ == "__main__":
    llenar_base_de_datos()
