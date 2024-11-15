-- PostgreSQL SQL Dump
-- Converted from MySQL/MariaDB format

BEGIN;

-- Crear la base de datos (opcional si ya está creada)
-- CREATE DATABASE bdd;
-- \c bdd;

-- Tabla: homicidios
CREATE TABLE homicidios (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    entidad VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    num_muertos INTEGER DEFAULT 0,
    hombres INTEGER DEFAULT 0,
    mujeres INTEGER DEFAULT 0,
    no_identificado INTEGER DEFAULT 0,
    fuente VARCHAR(255) NOT NULL DEFAULT '',  -- Cambié a NOT NULL
);


COMMIT;

-- Para importar los datos de la tabla, puedes usar COPY o importar el archivo CSV directamente.

-- Ejemplo para importar homicidios.csv
-- (Asegúrate de que homicidios.csv esté limpio y tenga las columnas en el mismo orden)
COPY homicidios (entidad, municipio, num_muertos, hombres, mujeres, no_identificado, fuente, fecha)
FROM '/ruta/a/homicidios.csv'
DELIMITER ','
CSV HEADER;
