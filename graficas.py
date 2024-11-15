# graficas.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import importlib.util

def cargar_modulo(ruta_archivo):
    spec = importlib.util.spec_from_file_location("modulo", ruta_archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

conectdb = cargar_modulo('conectdb.py')

def cargar_datos():
    conn = conectdb.conectar_a_base_datos()
    if conn:
        try:
            homicidios_df = pd.read_sql_query("SELECT * FROM homicidios;", conn)
            conn.close()
            return homicidios_df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
    return None

def filtrar_datos(homicidios_df, fecha_inicio, fecha_fin, municipio, genero):
    if fecha_inicio and fecha_fin:
        homicidios_df = homicidios_df[
            (homicidios_df['fecha'] >= fecha_inicio) &
            (homicidios_df['fecha'] <= fecha_fin)
        ]
    if municipio:
        homicidios_df = homicidios_df[homicidios_df['municipio'].str.contains(municipio, case=False, na=False)]
    if genero == "Hombres":
        homicidios_df = homicidios_df[homicidios_df['hombres'] > 0]
    elif genero == "Mujeres":
        homicidios_df = homicidios_df[homicidios_df['mujeres'] > 0]
    elif genero == "No Identificado":
        homicidios_df = homicidios_df[homicidios_df['no_identificado'] > 0]
    return homicidios_df

def graficar_datos(homicidios_df, tipo_grafico):
    if tipo_grafico == "Distribución de Homicidios por Género":
        total_por_genero = homicidios_df[["hombres", "mujeres", "no_identificado"]].sum()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(total_por_genero, labels=["Hombres", "Mujeres", "No Identificado"], autopct="%1.1f%%", colors=["blue", "pink", "gray"])
        ax.set_title("Distribución de Homicidios por Género")
        st.pyplot(fig)

    elif tipo_grafico == "Total de Muertos por Municipio":
        homicidios_por_municipio = homicidios_df.groupby("municipio")["num_muertos"].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(homicidios_por_municipio.index, homicidios_por_municipio.values, color="skyblue")
        ax.set_xlabel("Número de Muertos")
        ax.set_ylabel("Municipio")
        ax.set_title("Top 10 Municipios con Mayor Número de Homicidios")
        st.pyplot(fig)

    elif tipo_grafico == "Comparación de Homicidios por Género y Municipio":
        homicidios_por_genero = homicidios_df.groupby("municipio")[["hombres", "mujeres", "no_identificado"]].sum().head(10)
        homicidios_por_genero.plot(kind="bar", stacked=True, figsize=(10, 6), color=["blue", "pink", "gray"])
        plt.title("Comparación por Género en los Principales Municipios")
        plt.xlabel("Municipios")
        plt.ylabel("Cantidad")
        st.pyplot(plt)

def main():
    st.title("Dashboard Interactivo de Homicidios en México")
    st.markdown("""
    Este dashboard permite explorar y analizar datos de homicidios registrados en México.
    Puedes usar los filtros de la barra lateral para personalizar los datos mostrados.
    """)

    homicidios_df = cargar_datos()

    if homicidios_df is not None:
        st.sidebar.header("Filtros de Análisis")
        fecha_inicio = st.sidebar.date_input("Fecha Inicio", value=pd.to_datetime(homicidios_df["fecha"].min()))
        fecha_fin = st.sidebar.date_input("Fecha Fin", value=pd.to_datetime(homicidios_df["fecha"].max()))
        municipio = st.sidebar.text_input("Municipio")
        genero = st.sidebar.selectbox("Género", ["Todos", "Hombres", "Mujeres", "No Identificado"])

        homicidios_filtrados = filtrar_datos(homicidios_df, fecha_inicio, fecha_fin, municipio, genero if genero != "Todos" else None)

        st.write("### Datos Filtrados")
        st.dataframe(homicidios_filtrados)

        st.write("### Tablas Resumidas")
        
        # Tabla resumida por Municipio
        st.write("**Por Municipio:**")
        # Filtrar solo las columnas numéricas
        numeric_df = homicidios_filtrados.select_dtypes(include=['float64', 'int64'])
        if not numeric_df.empty:  # Verifica si hay columnas numéricas
            resumen_municipal = numeric_df.groupby(homicidios_filtrados['municipio']).sum()
            st.dataframe(resumen_municipal)

        # Tabla resumida por Fecha
        st.write("**Por Fecha:**")
        if not numeric_df.empty:  # Verifica si hay columnas numéricas
            resumen_fecha = numeric_df.groupby(homicidios_filtrados['fecha']).sum()
            st.dataframe(resumen_fecha)
    else:
        st.error("No se pudieron cargar los datos. Verifica la conexión a la base de datos.")

if __name__ == "__main__":
    main()
