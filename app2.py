import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página para diseño amplio
st.set_page_config(page_title="Dashboard de Homicidios", layout="wide")

# CSS para personalizar el diseño
custom_css = """
<style>
.main .block-container {
    max-width: 1800px; /* Ancho máximo */
    margin: 0 auto;
    padding: 20px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Parámetros de conexión a PostgreSQL
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1qaz2wsx',
    'host': 'localhost',
    'port': 5432
}

# Función para conectar a la base de datos
@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except psycopg2.Error as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

# Función para ejecutar consultas
def execute_query(query):
    conn = get_connection()
    if conn:
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
            return None
    else:
        return None

# Consultas SQL
query_total_muertos = """
    SELECT 
        e.nombre_entidad AS entidad,
        SUM(h.muertos) AS total_muertos,
        SUM(h.hombre) AS total_hombres,
        SUM(h.mujer) AS total_mujeres,
        SUM(h.no_identificado) AS total_no_identificados
    FROM hechos h
    JOIN municipios m ON h.id_municipio = m.id_municipio
    JOIN entidades e ON m.id_entidad = e.id_entidad
    GROUP BY e.nombre_entidad
    ORDER BY total_muertos DESC;
"""

query_tendencia = """
    SELECT 
        fecha, 
        SUM(muertos) AS total_muertos,
        SUM(hombre) AS total_hombres,
        SUM(mujer) AS total_mujeres
    FROM hechos
    GROUP BY fecha
    ORDER BY fecha ASC;
"""

query_totales = """
    SELECT 
        SUM(h.hombre) AS total_hombres,
        SUM(h.mujer) AS total_mujeres
    FROM hechos h;
"""

# Función para formatear los nombres de las columnas
def format_column_names(df):
    df.columns = [col.replace("_", " ").title() for col in df.columns]  # Capitaliza cada palabra
    return df


##############################################################################################################################################################

# Interfaz del dashboard
st.title("Dashboard de Homicidios")

tab1, tab2, tab3 = st.tabs(["Dashboard General", "Análisis por Género","Analisis temporal por Mes"])

##############################################################################################################################################################

with tab1:


    # Gráfico de tendencia temporal
    st.subheader("Tendencia de Homicidios")
    df_tendencia = execute_query(query_tendencia)

    if df_tendencia is not None:
        # Convertir las fechas al formato correcto explícitamente (YYYY-DD-MM)
        df_tendencia['fecha'] = pd.to_datetime(df_tendencia['fecha'], format='%Y-%d-%m')

        # Obtener el rango de fechas mínimo y máximo
        min_fecha = df_tendencia['fecha'].min().date()
        max_fecha = df_tendencia['fecha'].max().date()

        # Crear un slider para seleccionar el rango de fechas
        rango_fechas = st.slider(
            "Selecciona el rango de fechas",
            min_value=min_fecha,
            max_value=max_fecha,
            value=(min_fecha, max_fecha),  # Valores por defecto: todo el rango
            format="DD-MM-YYYY"  # Mostrar correctamente el formato
        )

        # Filtrar el DataFrame con el rango de fechas seleccionado
        df_filtrado = df_tendencia[
            (df_tendencia['fecha'] >= pd.Timestamp(rango_fechas[0])) & 
            (df_tendencia['fecha'] <= pd.Timestamp(rango_fechas[1]))
        ]

        # Calcular totales para el rango de fechas
        total_homicidios = df_filtrado['total_muertos'].sum()
        total_hombres = df_filtrado['total_hombres'].sum()
        total_mujeres = df_filtrado['total_mujeres'].sum()

        # Crear columnas para dividir el espacio
        col1, col2, col3, col4 = st.columns([7, 1, 1, 1])  # Relación de tamaño: 3 para el gráfico, 1 para los totales

        with col1:
            # Graficar la tendencia filtrada
            st.line_chart(df_filtrado.set_index("fecha"))

        with col2:
            st.metric(label="Homicidios Totales", value=f"{total_homicidios:,}")  # Formato con comas
        
        with col3:
            st.metric(label="Hombres", value=f"{total_hombres:,}")  # Total de hombres
        
        with col4:
            st.metric(label="Mujeres", value=f"{total_mujeres:,}")  # Total de mujeres

    ##############################################################################################################################################################

    # Fila 2: Resumen por entidad y gráfica de comparación
    col1, col2, col3 = st.columns([1, .7, .65])

    with col1:
        st.subheader("Resumen por Entidad")
        df_total_muertos = execute_query(query_total_muertos)
        if df_total_muertos is not None:
            df_total_muertos = format_column_names(df_total_muertos)
            st.dataframe(df_total_muertos)

    with col2:
        st.subheader("Top 5 Entidades con Más Homicidios")
        if df_total_muertos is not None:
            # Asegúrate de que las columnas tengan el formato correcto
            df_total_muertos = format_column_names(df_total_muertos)

            # Ordenar las entidades por número de homicidios y seleccionar las 5 primeras
            top_5_entidades = df_total_muertos.nlargest(5, 'Total Muertos')  # Usar el nombre capitalizado
            categorias = top_5_entidades['Entidad']
            valores = top_5_entidades['Total Muertos']
            
            # Crear la gráfica
            fig, ax = plt.subplots(figsize=(6, 2.5))
            fig.patch.set_facecolor('#111111')  # Fondo negro para toda la figura
            ax.set_facecolor('#111111')  # Fondo negro para el área de la gráfica
            ax.barh(categorias, valores, color='#10177a')  # Barras en azul

            # Estilo de texto: letras en blanco
            ax.set_title("Top 5 Entidades con Más Homicidios", color='white')
            ax.set_xlabel("Número de Homicidios", color='white')
            ax.set_ylabel("Entidades", color='white')
            ax.tick_params(colors='white')  # Colores de los ejes

            # Mostrar la gráfica
            st.pyplot(fig)


    with col3:
        st.subheader("Filtrar por Entidad")
        if df_total_muertos is not None:
            # Formatear nombres de columnas
            df_total_muertos = format_column_names(df_total_muertos)
            entidad = st.selectbox(
                "Selecciona una entidad:",
                df_total_muertos["Entidad"].unique()  # Usar "Entidad" capitalizado
            )

            if entidad:
                query_filtrado = f"""
                    SELECT 
                        m.nombre_municipio AS municipio,
                        SUM(h.muertos) AS total_muertos,
                        SUM(h.hombre) AS total_hombres,
                        SUM(h.mujer) AS total_mujeres
                    FROM hechos h
                    JOIN municipios m ON h.id_municipio = m.id_municipio
                    JOIN entidades e ON m.id_entidad = e.id_entidad
                    WHERE e.nombre_entidad = '{entidad}'
                    GROUP BY m.nombre_municipio
                    ORDER BY total_muertos DESC;
                """
                df_filtrado = execute_query(query_filtrado)
                if df_filtrado is not None:
                    df_filtrado = format_column_names(df_filtrado)
                    st.dataframe(df_filtrado)


##############################################################################################################################################################

with tab2:
    # Fila para gráfica de pastel y tablas
    st.subheader("Distribución de Homicidios por Género y Entidades")
    if df_tendencia is not None and df_total_muertos is not None:
        # Calcular totales para la gráfica de pastel
        total_hombres = df_tendencia['total_hombres'].sum()
        total_mujeres = df_tendencia['total_mujeres'].sum()

        # Datos para la gráfica
        categorias = ['Hombres', 'Mujeres']
        valores = [total_hombres, total_mujeres]
        colores = ['#10177a', '#a4549d']  # Colores personalizados

        # Crear columnas para dividir el espacio
        col1, col2, col3 = st.columns([.8, 1, .8])

        with col2:
            # Crear la gráfica de pastel
            fig, ax = plt.subplots(figsize=(5, 5))
            wedges, texts, autotexts = ax.pie(
                valores,
                labels=categorias,
                autopct='%1.1f%%',  # Mostrar porcentajes
                startangle=90,  # Rotar la gráfica
                colors=colores,  # Colores personalizados
                textprops={'color': 'white', 'fontsize': 10}  # Reducir tamaño del texto
            )

            # Ajustar tamaño del texto de los porcentajes
            for autotext in autotexts:
                autotext.set_fontsize(10)

            # Personalizar el fondo
            fig.patch.set_facecolor('#111111')  # Fondo negro para la figura
            ax.set_facecolor('#111111')  # Fondo negro para el área de la gráfica

            # Título de la gráfica
            ax.set_title("Distribución de Homicidios por Género", color='white', fontsize=14)

            # Mostrar la gráfica
            st.pyplot(fig)

        with col1:
            st.subheader("Hombres y Mujeres por Entidad")
            if df_total_muertos is not None:
                df_total_muertos = format_column_names(df_total_muertos)  # Asegúrate de que las columnas estén formateadas
                df_hombres_mujeres = df_total_muertos[['Entidad', 'Total Hombres', 'Total Mujeres']]
                st.dataframe(df_hombres_mujeres)


        with col3:
            st.subheader("Top 5 Entidades con Más Homicidios de Mujeres")
            if df_total_muertos is not None:
                df_total_muertos = format_column_names(df_total_muertos)  # Asegúrate de formatear los nombres
                top_5_mujeres = df_total_muertos.nlargest(5, 'Total Mujeres')[['Entidad', 'Total Mujeres']]
                st.dataframe(top_5_mujeres)


            # Tabla con Top 5 de entidades con más homicidios de hombres
            st.subheader("Top 5 Entidades con Más Homicidios de Hombres")
            if df_total_muertos is not None:
                top_5_hombres = df_total_muertos.nlargest(5, 'Total Hombres')[['Entidad', 'Total Hombres']]
                st.dataframe(top_5_hombres)


#######################################################################################################################################################


with tab3:

    st.subheader("Comparativa de Homicidios y Totales por Entidad")
    col1, col2 = st.columns([3, 2])  # Ajustar tamaño de columnas
    with col1:
        # Selector de las dos entidades
        entidades_disponibles = df_total_muertos["Entidad"].unique() if df_total_muertos is not None else []
        entidad_1 = st.selectbox("Selecciona la primera entidad:", entidades_disponibles, key="entidad_1")
        entidad_2 = st.selectbox("Selecciona la segunda entidad:", entidades_disponibles, key="entidad_2")

        if entidad_1 and entidad_2:
            # Consulta para la primera entidad
            query_filtrado_1 = f"""
                SELECT 
                    DATE_TRUNC('month', h.fecha) AS mes,
                    SUM(h.muertos) AS total_muertos
                FROM hechos h
                JOIN municipios m ON h.id_municipio = m.id_municipio
                JOIN entidades e ON m.id_entidad = e.id_entidad
                WHERE e.nombre_entidad = '{entidad_1}'
                GROUP BY mes
                ORDER BY mes;
            """
            df_entidad_1 = execute_query(query_filtrado_1)

            # Consulta para la segunda entidad
            query_filtrado_2 = f"""
                SELECT 
                    DATE_TRUNC('month', h.fecha) AS mes,
                    SUM(h.muertos) AS total_muertos
                FROM hechos h
                JOIN municipios m ON h.id_municipio = m.id_municipio
                JOIN entidades e ON m.id_entidad = e.id_entidad
                WHERE e.nombre_entidad = '{entidad_2}'
                GROUP BY mes
                ORDER BY mes;
            """
            df_entidad_2 = execute_query(query_filtrado_2)

            if df_entidad_1 is not None and df_entidad_2 is not None:
                # Convertir las fechas truncadas a datetime
                df_entidad_1['mes'] = pd.to_datetime(df_entidad_1['mes'])
                df_entidad_2['mes'] = pd.to_datetime(df_entidad_2['mes'])

                # Unir ambos DataFrames para comparación
                df_comparativa = pd.merge(
                    df_entidad_1.rename(columns={"total_muertos": f"{entidad_1}"}),
                    df_entidad_2.rename(columns={"total_muertos": f"{entidad_2}"}),
                    on="mes",
                    how="outer"
                ).fillna(0)

                # Crear columnas para dividir el espacio
                

                
                    # Graficar la comparación
                st.line_chart(
                    df_comparativa.set_index("mes"),
                    width=700,
                    height=400
                )

            with col2:
                # Gráfica de barras general para todas las entidades
                st.subheader("Total de Homicidios por Entidad")
                total_por_entidad = df_total_muertos[['Entidad', 'Total Muertos']].sort_values(by='Total Muertos', ascending=False)

                st.bar_chart(
                    total_por_entidad.set_index("Entidad"),
                    width=500,
                    height=400
                )






