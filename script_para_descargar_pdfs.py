import requests
import os
from datetime import datetime, timedelta
import json
from pathlib import Path

# Define la URL base
base_url = "http://www.informeseguridad.cns.gob.mx/files/homicidios_{}.pdf"

# Ruta del archivo de configuración
config_file = Path.home() / '.config' / 'pdf_directory_config.json'

# Función para cargar o establecer el directorio de PDFs
def get_pdf_directory():
    if config_file.exists():
        # Cargar el directorio desde el archivo de configuración
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('pdf_directory')
    else:
        # Preguntar al usuario por la ubicación inicial
        default_dir = Path.home() / 'Documents' / 'PDFs'
        user_dir = input(f"Introduce el directorio para almacenar los PDFs (presiona Enter para usar la ruta predeterminada: {default_dir}): ")
        pdf_directory = Path(user_dir.strip()) if user_dir.strip() else default_dir
        os.makedirs(pdf_directory, exist_ok=True)

        # Guardar el directorio en el archivo de configuración
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump({'pdf_directory': str(pdf_directory)}, f)

        return pdf_directory

# Función para descargar los PDFs basados en las fechas de inicio y fin
def descargar_pdfs(fecha_inicio, fecha_fin):
    pdf_directory = get_pdf_directory()
    
    current_date = fecha_inicio
    while current_date <= fecha_fin:
        date_str = current_date.strftime("%Y%m%d")
        pdf_url = base_url.format(date_str)
        response = requests.get(pdf_url)

        if response.status_code == 200:
            with open(os.path.join(pdf_directory, f"homicidios_{date_str}.pdf"), 'wb') as f:
                f.write(response.content)
            print(f"Descargado: {pdf_url}")
        else:
            print(f"No se encontró el archivo: {pdf_url}")

        current_date += timedelta(days=1)

# La función de entrada para pruebas o ejecución directa sería opcional, pero asegúrate de no ejecutarla al importar
if __name__ == "__main__":
    # Puede permanecer vacío ya que estás llamando estas funciones desde otro lugar
    pass
