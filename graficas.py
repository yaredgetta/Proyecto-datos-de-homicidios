import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For boxplots and enhanced visualizations
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

            # Ensure that 'fecha' is a datetime type
            homicidios_df['fecha'] = pd.to_datetime(homicidios_df['fecha'], errors='coerce')

            return homicidios_df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
    return None


def filtrar_datos(homicidios_df, fecha_inicio, fecha_fin, municipios, genero):
    if fecha_inicio and fecha_fin:
        homicidios_df = homicidios_df[
            (homicidios_df['fecha'] >= fecha_inicio) &
            (homicidios_df['fecha'] <= fecha_fin)
        ]
    if municipios:
        homicidios_df = homicidios_df[homicidios_df['municipio'].isin(municipios)]

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
        homicidios_por_genero = homicidios_df.groupby("municipio")[["hombres", "mujeres", "no_identificado"]].sum()
        homicidios_por_genero.plot(kind="bar", stacked=True, figsize=(10, 6), color=["blue", "pink", "gray"])
        plt.title("Comparación por Género en los Municipios Seleccionados")
        plt.xlabel("Municipios")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif tipo_grafico == "Histograma de Homicidios":
        plt.figure(figsize=(10, 6))
        sns.histplot(homicidios_df['num_muertos'], bins=20, kde=True)
        plt.title("Distribución de Homicidios")
        plt.xlabel("Número de Muertos")
        plt.ylabel("Frecuencia")
        st.pyplot(plt)

    elif tipo_grafico == "Tendencia Mensual de Homicidios":
        homicidios_df['mes_año'] = homicidios_df['fecha'].dt.to_period('M')
        tendencia_mensual = homicidios_df.groupby('mes_año')['num_muertos'].sum().reset_index()
        tendencia_mensual['mes_año'] = tendencia_mensual['mes_año'].dt.to_timestamp()

        plt.figure(figsize=(10, 6))
        plt.plot(tendencia_mensual['mes_año'], tendencia_mensual['num_muertos'], marker='o')
        plt.title("Tendencia Mensual de Homicidios")
        plt.xlabel("Mes")
        plt.ylabel("Total de Homicidios")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif tipo_grafico == "Box Plot de Homicidios por Municipio":
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='municipio', y='num_muertos', data=homicidios_df)
        plt.title("Box Plot de Homicidios por Municipio")
        plt.xlabel("Municipio")
        plt.ylabel("Número de Muertos")
        plt.xticks(rotation=45)
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
        
        # Ensure date inputs are treated as pd.Timestamp
        fecha_inicio = pd.to_datetime(st.sidebar.date_input("Fecha Inicio", value=pd.to_datetime(homicidios_df["fecha"].min())), format='%Y-%m-%d')
        fecha_fin = pd.to_datetime(st.sidebar.date_input("Fecha Fin", value=pd.to_datetime(homicidios_df["fecha"].max())), format='%Y-%m-%d')
        
        unique_municipios = homicidios_df['municipio'].unique()
        municipios = st.sidebar.multiselect("Selecciona Municipios", unique_municipios)

        genero = st.sidebar.selectbox("Género", ["Todos", "Hombres", "Mujeres", "No Identificado"])
        stat_type = st.sidebar.selectbox("Tipo de Estadística", ["Media", "Mediana", "Máximo", "Mínimo"])

        # Filter data
        homicidios_filtrados = filtrar_datos(homicidios_df, fecha_inicio, fecha_fin, municipios, genero if genero != "Todos" else None)

        st.write("### Datos Filtrados")
        st.dataframe(homicidios_filtrados)

        st.write("### Tablas Resumidas")
        st.write("**Por Municipio:**")
        numeric_df = homicidios_filtrados.select_dtypes(include=['float64', 'int64'])

        if not numeric_df.empty:
            resumen_municipal = numeric_df.groupby(homicidios_filtrados['municipio']).agg(['mean', 'median', 'max', 'min'])
            st.dataframe(resumen_municipal)

        st.write("**Por Fecha:**")
        if not numeric_df.empty:
            resumen_fecha = numeric_df.groupby(homicidios_filtrados['fecha']).agg(['mean', 'median', 'max', 'min'])
            st.dataframe(resumen_fecha)

        st.sidebar.header("Gráficos")
        tipo_grafico = st.sidebar.selectbox("Selecciona un gráfico", [
            "Distribución de Homicidios por Género",
            "Total de Muertos por Municipio",
            "Comparación de Homicidios por Género y Municipio",
            "Histograma de Homicidios",
            "Tendencia Mensual de Homicidios",
            "Box Plot de Homicidios por Municipio"
        ])

        graficar_datos(homicidios_filtrados, tipo_grafico)
    else:
        st.error("No se pudieron cargar los datos. Verifica la conexión a la base de datos.")

if __name__ == "__main__":
    main()
