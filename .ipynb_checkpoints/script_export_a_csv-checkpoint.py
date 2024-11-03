import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pandas as pd
import os

# Directorio donde se guardarán los PDFs descargados
pdf_directory = r'C:\Users\alexi\OneDrive\Desktop\adoo\pdfs'
output_csv = os.path.join(pdf_directory, 'DatosCrudos.csv')

# Configura Pytesseract para OCR (reemplaza la ruta con la ruta a tu ejecutable si es necesario)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Lista para almacenar el contenido extraído
extracted_data = []

def extract_text_from_pdf(pdf_path):
    """
    Extrae el texto de un PDF. Si el PDF contiene solo imágenes, utiliza OCR.
    """
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            
            # Intenta extraer texto directo
            text = page.get_text()
            
            if text.strip():  # Si hay texto, lo añadimos
                extracted_data.append({"page": page_num + 1, "text": text})
            else:
                # Si no hay texto, usa OCR en cada imagen de la página
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img)
                extracted_data.append({"page": page_num + 1, "text": text})

# Itera sobre los archivos en el directorio de PDFs
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"Procesando: {pdf_path}")
        extract_text_from_pdf(pdf_path)

# Guardar los datos extraídos en un archivo CSV
df = pd.DataFrame(extracted_data)
df.to_csv(output_csv, index=False, encoding='utf-8')
print(f"Datos crudos guardados en {output_csv}")
