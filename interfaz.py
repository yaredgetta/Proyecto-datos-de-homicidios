# interfaz.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Create SQLAlchemy engine
def create_engine_connection():
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    return create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

engine = create_engine_connection()

@st.cache_data
def cargar_dataframe():
    query = "SELECT * FROM homicidios"
    return pd.read_sql(query, engine)

def actualizar_base_de_datos(dataframe):
    dataframe.to_sql('homicidios', engine, if_exists='replace', index=False)
