-- PostgreSQL SQL Dump
-- Converted from MySQL/MariaDB format

BEGIN;

-- Crear la base de datos (opcional si ya está creada)
-- CREATE DATABASE bdd;
-- \c bdd;

-- Tabla: entidades
CREATE TABLE entidades (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    poblacion INTEGER NOT NULL DEFAULT 0,  -- Cambié a NOT NULL
    region VARCHAR(100) NOT NULL DEFAULT '',  -- Cambié a NOT NULL
);

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

-- Tabla: usuarios
CREATE TABLE usuarios (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rol VARCHAR(50) NOT NULL DEFAULT '',  -- Cambié a NOT NULL
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMIT;

-- Para importar los datos de la tabla, puedes usar COPY o importar el archivo CSV directamente.

-- Ejemplo para importar homicidios.csv
-- (Asegúrate de que homicidios.csv esté limpio y tenga las columnas en el mismo orden)
COPY homicidios (entidad, municipio, num_muertos, hombres, mujeres, no_identificado, fuente, fecha)
FROM '/ruta/a/homicidios.csv'
DELIMITER ','
CSV HEADER;
