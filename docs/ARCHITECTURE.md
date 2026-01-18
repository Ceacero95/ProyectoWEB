
# Arquitectura del Proyecto de Datos de Energía (ESIOS/OMIE)

## Visión General
Este proyecto implementa un pipeline de ingestión y procesamiento de datos del mercado eléctrico ibérico (OMIE) y del sistema eléctrico (ESIOS). El objetivo es automatizar la descarga, limpieza y almacenamiento de estos datos para su posterior análisis.

## Estructura del Pipeline (Medallion Architecture)
El proyecto sigue la arquitectura de capas estándar:

### 1. Capa Bronze (Raw)
*   **Objetivo**: Almacenar los datos "crudos" tal cual vienen de la fuente.
*   **Formato**: ZIP, JSON, CSV.
*   **Ubicación**: `local_data/bronze/` (o Bucket GCS en producción).
*   **Responsabilidad**: `src/bronze/`
    *   Descarga idempotente (chequea si existe antes de descargar).
    *   Organización por carpetas `YYYY/MM`.

### 2. Capa Silver (Cleaned)
*   **Objetivo**: Limpiar, normalizar y estructurar los datos.
*   **Formato**: Parquet (intermedio) y Tablas SQL (PostgreSQL).
*   **Ubicación**: 
    *   Ficheros: `local_data/silver/`
    *   BBDD: Schema `omie` / `esios`.
*   **Responsabilidad**: `src/silver/`
    *   Parsing de ficheros extraños (CSV con cabeceras complejas).
    *   Normalización de nombres de columnas (Regex).
    *   Tipado de datos (Fechas, Floats con coma).
    *   **Idempotencia**: Borrado de datos previos para la misma fecha antes de insertar.

### 3. Capa Gold (Consumption) - *Futuro*
*   **Objetivo**: Vistas agregadas y métricas listas para BI.
*   **Tecnología**: Vistas SQL o Tablas específicas en BigQuery.

## Tecnologías Clave
*   **Python 3.9+**: Lenguaje principal.
*   **Apache Airflow**: Orquestación de tareas diarias.
*   **PostgreSQL**: Base de datos relacional operativa.
*   **SQLAlchemy**: ORM/Query Builder.
*   **Pandas**: Manipulación de datos en memoria.
*   **Docker**: Contenerización para despliegue reproducible.
