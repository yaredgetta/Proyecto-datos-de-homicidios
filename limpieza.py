import pandas as pd

# Cargar el archivo CSV
input_csv = 'pdfs/Datos_1/0CT_1.csv'
df = pd.read_csv(input_csv)

# Lista de entidades y municipios válidos (simplificada para este ejemplo)
valid_entities = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", 
    "Chihuahua", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", 
    "Hidalgo", "Jalisco", "Mexico City", "Michoacan", "Morelos", "Nayarit", 
    "Nuevo Leon", "Oaxaca", "Puebla", "Queretaro", "Quintana Roo", 
    "San Luis Potosi", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", 
    "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"
]

valid_municipalities = [
    # Esta lista debería contener todos los municipios de México
    "Mexicali", "Tijuana", "La Paz", "Villaflores", "Jiménez", "Juárez", "San Juan de Sabinas",
    "Colima", "Celaya", "León", "Pénjamo", "Salamanca", "Salvatierra", "Silao de la Victoria",
    "Tarimoro", "Valle de Santiago", "Atoyac de Álvarez", "Morelia", "Juárez", "Monterrey",
    "Cuautinchán", "Puebla", "Benito Juárez", "Culiacán", "Santa Ana", "Cárdenas", "Natívitas",
    "San Pablo del Monte", "Las Vigas de Ramírez", "Río Blanco", "Guadalupe"
]

# Función para validar y limpiar los datos
def is_valid_row(row):
    entidad = row['Entidad']
    municipio = row['Municipio']
    num_muertos = row['Numero de muertos']
    sexo_hombre = row['Sexo (Hombre)']
    sexo_mujer = row['Sexo (Mujer)']
    num_identificado = row['Numero de identificado']
    fuente = row['Fuente']
    
    # Validar los datos
    if entidad in valid_entities and municipio in valid_municipalities:
        if str(num_muertos).isdigit() and (str(sexo_hombre).isdigit() or sexo_hombre == '-') and (str(sexo_mujer).isdigit() or sexo_mujer == '-'):
            if str(num_identificado).isdigit() or num_identificado == '-':
                return True
    return False

# Aplicar la función de validación y limpieza
cleaned_df = df[df.apply(is_valid_row, axis=1)]

# Guardar los datos limpiados en un nuevo archivo CSV
output_csv = '0CT_1_cleaned.csv'
cleaned_df.to_csv(output_csv, index=False, encoding='utf-8')

print(f"Datos limpiados guardados en {output_csv}")
