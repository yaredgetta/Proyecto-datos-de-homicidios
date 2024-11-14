import os
import pdfplumber
import pandas as pd
import unicodedata
from datetime import datetime
from pathlib import Path
import json

# Ruta a la carpeta de PDFs desde el archivo de configuración
config_file = Path.home() / '.config' / 'pdf_directory_config.json'

# Función para cargar el directorio de configuración
def load_pdf_directory():
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('pdf_directory')
    else:
        raise FileNotFoundError(
            f"No se encontró el archivo de configuración: {config_file}. "
            "Por favor, ejecuta el primer script para configurarlo."
        )

# Cargar el directorio de PDFs
try:
    pdf_directory = load_pdf_directory()
except FileNotFoundError as e:
    print(e)
    exit(1)

# Ruta a la carpeta de salida
output_folder = os.path.join(pdf_directory, "Datacsv")
os.makedirs(output_folder, exist_ok=True)

# Función para normalizar texto eliminando acentos y caracteres especiales
def normalize_text(text):
    if isinstance(text, str):
        # Normaliza eliminando acentos y caracteres especiales
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

# Función para verificar si un PDF contiene texto
def es_pdf_con_texto(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():  # Si encuentra texto en alguna página
                return True
    return False  # No se encontró texto en ninguna página

# Función para convertir tablas de un PDF a CSV, con normalización de texto y validación de columnas
def pdf_table_to_csv_with_normalization(pdf_path, csv_path):
    # Verificar si el PDF contiene texto antes de procesarlo
    if not es_pdf_con_texto(pdf_path):
        print(f"El archivo {pdf_path} no contiene texto y se omitirá.")
        return  # Omitir el procesamiento si el PDF no tiene texto

    # Extraer fecha del nombre del archivo
    try:
        date_str = os.path.basename(pdf_path).split('_')[1].replace(".pdf", "")
        date_obj = datetime.strptime(date_str, "%d%m%Y")  # Convierte '21092024' a formato datetime
    except (IndexError, ValueError):
        print(f"No se pudo extraer una fecha válida del archivo {pdf_path}.")
        date_obj = None  # Usa None como valor por defecto si no se encuentra fecha

    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and row[0] not in ["Entidad", "Municipio", "Muertos", "Hombre", "Mujer", "No Identificado", "Fuente"]:
                        # Aplica normalización a cada celda en la fila
                        normalized_row = [normalize_text(cell) for cell in row]
                        if date_obj:
                            normalized_row.append(date_obj)  # Añade la fecha al final de la fila
                        data.append(normalized_row)

    # Definir columnas del DataFrame
    columns = ["Entidad", "Municipio", "Muertos", "Hombre", "Mujer", "No Identificado", "Fuente"]
    if date_obj:
        columns.append("Fecha")

    # Crear DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Limpieza de datos
    df = df[~df['Entidad'].isin(['Homicidios Dolosos', 'No de Muertos'])].reset_index(drop=True)
    numeric_columns = ['Muertos', 'Hombre', 'Mujer', 'No Identificado']
    df[numeric_columns] = df[numeric_columns].replace('-', 0)
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    # Guarda el DataFrame limpio en un archivo CSV con codificación UTF-8
    df.to_csv(csv_path, index=False, encoding='utf-8')

# Recorre todos los archivos PDF en la carpeta de entrada y convierte cada uno a CSV
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        csv_filename = filename.replace(".pdf", ".csv")
        csv_path = os.path.join(output_folder, csv_filename)
        pdf_table_to_csv_with_normalization(pdf_path, csv_path)
        print(f"Convertido: {filename} a {csv_filename}")
