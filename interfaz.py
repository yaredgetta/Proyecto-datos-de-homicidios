import streamlit as st
import pandas as pd
import sqlalchemy

# Configura la conexión a la base de datos
engine = sqlalchemy.create_engine('postgresql://postgres:Gta7613205@localhost:5432/Homicidios')

# Cargar datos
@st.cache
def cargar_datos():
    query = "SELECT * FROM homicidios"
    return pd.read_sql(query, engine)

# Cargar los datos y mostrarlos en una tabla
df = cargar_datos()

st.title("Tabla de Homicidios Dolosos")
st.dataframe(df)  # Muestra la tabla con los datos
