# limpieza.py
import pandas as pd

def limpiar_datos(homicidios_df):
    # Example cleaned approach; you must pass the dataframe to the function
    homicidios_df_cleaned = homicidios_df.drop(columns=["Unnamed: 0"])
    homicidios_df_cleaned['fecha'] = pd.to_datetime(homicidios_df_cleaned['fecha'], errors='coerce')
    homicidios_df_cleaned['municipio'] = homicidios_df_cleaned['municipio'].fillna('Desconocido')
    homicidios_df_cleaned['entidad'] = homicidios_df_cleaned['entidad'].fillna('Desconocido')
    return homicidios_df_cleaned  # Ensure it returns the cleaned dataframe
