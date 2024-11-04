import os
import pdfplumber
import pandas as pd

# Ruta a la carpeta con archivos PDF
input_folder = "C:/Users/alexi/OneDrive/Desktop/adoo/pdfs"
output_folder = "C:/Users/alexi/OneDrive/Desktop/adoo/csvs"

# Crea la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Función para convertir tablas de un solo PDF a CSV
def pdf_table_to_csv(pdf_path, csv_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extrae las tablas de la página actual
            tables = page.extract_tables()
            
            # Procesa cada tabla en la página
            for table in tables:
                # Añade cada fila de la tabla a `data`
                for row in table:
                    if row:  # Ignora filas vacías
                        data.append(row)
    
    # Convierte los datos extraídos en un DataFrame de pandas
    df = pd.DataFrame(data, columns=["Entidad", "Municipio", "Muertos", "Hombre", "Mujer", "No Identificado", "Fuente"])
    df.to_csv(csv_path, index=False, encoding='utf-8')

# Recorre todos los archivos PDF en la carpeta de entrada y convierte cada uno a CSV
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        csv_filename = filename.replace(".pdf", ".csv")
        csv_path = os.path.join(output_folder, csv_filename)
        pdf_table_to_csv(pdf_path, csv_path)
        print(f"Convertido: {filename} a {csv_filename}")
