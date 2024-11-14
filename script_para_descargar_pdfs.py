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







# Itera sobre cada día en el rango de fechas
current_date = start_date
while current_date <= end_date:
    # Formatea la fecha en el formato requerido (ddmmyyyy)
    formatted_date = current_date.strftime('%d%m%Y')
    
    # Genera la URL del PDF
    pdf_url = base_url.format(formatted_date)
    
    # Verifica el enlace antes de descargar
    print(f"Descargando: {pdf_url}")
    
    # Realiza la solicitud para obtener el PDF
    pdf_response = requests.get(pdf_url)

    # Verifica si la solicitud fue exitosa
    if pdf_response.status_code == 200:
        pdf_name = os.path.join(pdf_directory, f'homicidios_{formatted_date}.pdf')  # Nombre del archivo
        with open(pdf_name, 'wb') as f:
            f.write(pdf_response.content)
        print(f"Descargado: {pdf_name}")
    else:
        print(f"Error al descargar {pdf_url}: {pdf_response.status_code}")

    # Avanza al siguiente día
    current_date += timedelta(days=1)
