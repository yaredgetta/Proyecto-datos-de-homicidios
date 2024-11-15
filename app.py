# app.py
import streamlit as st
import importlib.util
import os
from datetime import datetime

# Set Streamlit page config at the start
st.set_page_config(page_title="Aplicación de Gestión de Homicidios", layout="wide")

# Function to load modules from local files
def cargar_modulo(ruta_archivo):
    spec = importlib.util.spec_from_file_location("modulo", ruta_archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

# Load necessary modules
conectdb = cargar_modulo('conectdb.py')
interfaz = cargar_modulo('interfaz.py')
graficas = cargar_modulo('graficas.py')
script_para_descargar = cargar_modulo('script_para_descargar_pdfs.py')
script_export_a_csv = cargar_modulo('script_export_a_csv.py')
limpieza = cargar_modulo('limpieza.py')

# Create Streamlit interface
st.title('Aplicación de Gestión de Homicidios')

pagina = st.sidebar.radio('Selecciona una página:', ['Conexión a la base de datos', 'Gestión de datos', 'Gráficas'])

# Database Connection Page
if pagina == 'Conexión a la base de datos':
    st.header('Conexión a la base de datos')
    conexion = conectdb.conectar_a_base_datos()

    if conexion:
        st.success("Conexión exitosa a la base de datos.")
    else:
        st.error("No se pudo conectar a la base de datos.")

# Data Management Page
elif pagina == 'Gestión de datos':
    st.header('Gestión de datos en la base de datos')
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = interfaz.cargar_dataframe()

    st.write(st.session_state['dataframe'])

    # Button to update the database with the dataframe
    if st.button('Actualizar base de datos'):
        interfaz.actualizar_base_de_datos(st.session_state['dataframe'])
        st.success('Datos actualizados exitosamente en la base de datos.')

# Graphs Page
elif pagina == 'Gráficas':
    st.header('Gráficas de Homicidios')
    graficas.main()

# Download and Process Data Section
st.sidebar.header("Descargar y Procesar Datos")
fecha_inicio = st.sidebar.date_input("Fecha Inicio", value=datetime(2024, 1, 1))
fecha_fin = st.sidebar.date_input("Fecha Fin", value=datetime(2024, 12, 31))

if st.sidebar.button("Ejecutar Proceso"):
    with st.spinner("Descargando PDFs..."):
        script_para_descargar.descargar_pdfs(fecha_inicio, fecha_fin)
    st.success("Descarga de PDFs completada.")

    with st.spinner("Convirtiendo PDFs a CSV..."):
        script_export_a_csv.convertir_pdfs_a_csv()
    st.success("Conversión a CSV completada.")

    with st.spinner("Limpiando datos..."):
        limpieza.limpiar_datos()
    st.success("Limpieza de datos completada.")
