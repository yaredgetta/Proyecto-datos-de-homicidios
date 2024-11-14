# app.py
import streamlit as st
import importlib.util
import os

# Función para cargar módulos desde archivos locales
def cargar_modulo(ruta_archivo):
    spec = importlib.util.spec_from_file_location("modulo", ruta_archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

# Cargar los módulos necesarios
# Modificar las rutas según sea necesario
conectdb = cargar_modulo('conectdb.py')
interfaz = cargar_modulo('interfaz.py')
script_export_a_csv = cargar_modulo('script_export_a_csv.py')
script_para_descargar = cargar_modulo('script_para_descargar.py')

# Crear la interfaz en Streamlit
st.title('Aplicación de Gestión de Homicidios')

# Crear un menú de navegación usando radio button
pagina = st.sidebar.radio('Selecciona una página:', ['Conexión a la base de datos', 'Gestión de datos', 'Convertir PDF a CSV', 'Descargar PDFs sobre homicidios'])

# Página de Conexión a la base de datos
if pagina == 'Conexión a la base de datos':
    st.header('Conexión a la base de datos')
    conexion = conectdb.conectar_a_base_datos()

    if conexion:
        st.success("Conexión exitosa a la base de datos.")
    else:
        st.error("No se pudo conectar a la base de datos.")

# Página de Gestión de datos en la base de datos
elif pagina == 'Gestión de datos':
    st.header('Gestión de datos en la base de datos')
    # Usamos la interfaz definida en el archivo interfaz.py
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = interfaz.cargar_dataframe()

    # Mostrar el dataframe
    st.write(st.session_state['dataframe'])

    # Botón para actualizar la base de datos con el dataframe
    if st.button('Actualizar base de datos'):
        interfaz.actualizar_base_de_datos(st.session_state['dataframe'])
        st.success('Datos actualizados exitosamente en la base de datos.')

# Página para convertir PDF a CSV
elif pagina == 'Convertir PDF a CSV':
    st.header('Convertir PDF a CSV')
    archivo_pdf = st.file_uploader("Selecciona un archivo PDF para convertirlo a CSV", type=["pdf"])

    if archivo_pdf is not None:
        # Guardar temporalmente el archivo PDF
        if not os.path.exists("temp_pdf"):
            os.makedirs("temp_pdf")  # Crear carpeta si no existe
        with open(os.path.join("temp_pdf", archivo_pdf.name), "wb") as f:
            f.write(archivo_pdf.getbuffer())

        # Convertir el PDF a CSV usando el script
        ruta_pdf = os.path.join("temp_pdf", archivo_pdf.name)
        csv_output = script_export_a_csv.convertir_pdf_a_csv(ruta_pdf)

        st.write(f'El archivo CSV ha sido generado: {csv_output}')
        st.download_button("Descargar CSV", csv_output)

# Página para descargar PDFs sobre homicidios
elif pagina == 'Descargar PDFs sobre homicidios':
    st.header('Descargar PDFs sobre homicidios')
    anio = st.number_input("Ingresa el año para descargar los PDFs de homicidios", min_value=2000, max_value=2024, value=2023)

    if st.button('Descargar PDFs'):
        st.write("Iniciando descarga de PDFs...")
        pdfs_descargados = script_para_descargar.descargar_pdfs_homicidios(anio)
        st.write(f"Se han descargado {len(pdfs_descargados)} archivos PDF.")
        for pdf in pdfs_descargados:
            st.write(pdf)

