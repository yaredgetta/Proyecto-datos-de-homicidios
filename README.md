# Aplicación de Gestión de Datos de Homicidios

## Descripción General

La Aplicación de Gestión de Datos de Homicidios es una herramienta diseñada para la recolección, procesamiento, análisis y visualización de datos sobre homicidios desarrollada con Python, Streamlit y PostgreSQL. 

## Características Clave

- **Conexión a Datos**: Establece conexiones con bases de datos PostgreSQL utilizando configuraciones de entorno, permitiendo una interacción fluida con bases de datos locales.
- **Recolección de Datos**: Descarga datos de homicidios en formato PDF desde fuentes designadas, asegurando acceso oportuno a las estadísticas más recientes.
- **Procesamiento de Datos**: Convierte los datos en formato PDF a formato CSV, seguido de un proceso de limpieza y normalización para preparar los datos para su análisis.
- **Gestión de Datos**: Actualiza y gestiona conjuntos de datos sincronizando los datos limpios con la base de datos, proporcionando un repositorio actualizado para su análisis.
- **Visualización de Datos**: Genera visualizaciones útiles que ilustran tendencias y patrones en los casos de homicidio según los filtros definidos por el usuario (por ejemplo, rango de fechas, municipio, género).
- **Interfaz Fácil de Usar**: Una interfaz de aplicación web responsiva e intuitiva construida sobre Streamlit, haciéndola accesible a usuarios con diversos niveles de conocimiento técnico.

## Pila Técnica

- **Lenguaje de Programación**: Python
- **Framework Web**: Streamlit
- **Base de Datos**: PostgreSQL
- **Manipulación y Análisis de Datos**: Pandas
- **Visualización de Datos**: Matplotlib y funciones integradas de Streamlit
- **Procesamiento de PDFs**: pdfplumber
- **Gestión de Entorno**: dotenv para manejar configuraciones

## Instalación

### Requisitos Previos

Asegúrate de tener instalado lo siguiente:

- Python 3.6 o superior
- Base de Datos PostgreSQL

### Clonar el Repositorio

```bash
git clone https://github.com/yaredgetta/Proyecto-datos-de-homicidios.git
cd Proyecto-datos-de-homicidios
```

### Instalar las Bibliotecas Requeridas

Usa pip para instalar las dependencias necesarias listadas en el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Configuración del Entorno

Crea un archivo `.env` en el directorio del proyecto e incluye las siguientes variables de entorno:

```bash
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=homicidios
CSV_FOLDER=ruta/a/carpeta/csv
```

## Uso

### Ejecutar la Aplicación

Para iniciar la aplicación Streamlit, ejecuta:

```bash
streamlit run app.py
```

### Interfaz de la Aplicación

1. **Conexión a la Base de Datos**: Navega a la página "Conexión a la base de datos" para probar o establecer una conexión con la base de datos PostgreSQL.
2. **Gestión de Datos**: En la página "Gestión de datos", visualiza y actualiza los datos de homicidio almacenados en la base de datos.
3. **Visualización de Datos**: Usa la página "Gráficas" para seleccionar filtros y visualizaciones que te permitan explorar las tendencias en los datos de homicidios.
4. **Descargar y Procesar Datos**: Utiliza el panel lateral para definir rangos de fechas para descargar PDFs, convertirlos en archivos CSV limpios y procesar los datos.
