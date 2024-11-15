import requests
import os
from datetime import datetime, timedelta
import platform  # Import platform to check the operating system
import json
from pathlib import Path


# Define la URL base
base_url = "http://www.informeseguridad.cns.gob.mx/files/homicidios_{}.pdf"

# Define la fecha de inicio y la fecha de fin
start_date = datetime(2024, 9, 20)  # Fecha de inicio
end_date = datetime(2024, 10, 2)    # Fecha de fin

# Especifica el directorio para almacenar los PDFs basado en el sistema operativo
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

# Obtener el directorio de PDFs
pdf_directory = get_pdf_directory()
print(f"Los PDFs se guardarán en: {pdf_directory}")
