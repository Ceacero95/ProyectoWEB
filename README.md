# ProyectoWEB - ESIOS Data Manager

Este proyecto es una herramienta integral para la descarga, procesamiento y almacenamiento de datos del mercado eléctrico español (ESIOS). Está diseñado para automatizar la obtención de indicadores clave como precios de desvíos, participación de tecnologías, y ficheros de liquidación (Liquicomun).

## Estructura del Proyecto

El proyecto sigue una arquitectura modular y limpia, separando responsabilidades claramente:

```
ProyectoWEB/
├── manage.py           # Punto de entrada principal (CLI) para gestionar el proyecto.
├── .env                # Variables de entorno (Token ESIOS, credenciales DB).
├── requirements.txt    # Dependencias del proyecto.
├── local_data/         # (Ignorado) Almacenamiento local de ficheros descargados.
├── src/                # Código fuente principal.
│   ├── api/            # Servidor API (FastAPI) para exponer datos.
│   ├── config/         # Gestión de configuración y settings globales.
│   ├── db/             # Conexión y utilidades de base de datos.
│   ├── esios/          # Módulos de conexión con ESIOS API y lógica de descarga.
│   │   ├── client.py     # Cliente HTTP para la API de ESIOS.
│   │   └── downloader.py # Orquestador de descargas (Sync/Backfill).
│   ├── processors/     # Lógica de negocio para procesar ficheros específicos (ej. I90).
│   └── storage/        # Capa de persistencia (Sistema de ficheros local / GCS).
```

## Funcionalidades Principales

El sistema se gestiona principalmente a través de `manage.py`, que ofrece varios comandos:

1.  **Sincronización Diaria (`sync`)**:
    Descarga los ficheros configurados (I3, Liquicomun, I90) para el día en curso o un rango de fechas. Gestiona automáticamente la lógica de frecuencias (ej. algunos ficheros solo se bajan mensualmente).
    ```bash
    python manage.py sync
    ```

2.  **Backfill de Datos (`backfill`)**:
    Permite descargar datos históricos de un indicador o tipo de archivo específico.
    ```bash
    python manage.py backfill --archive-id <ID> --name <NOMBRE> --start-date YYYY-MM-DD
    ```

3.  **Servidor API (`server`)**:
    Levanta un servidor web para consultas en tiempo real (si aplica).
    ```bash
    python manage.py server
    ```

## Configuración

1.  **Entorno Virtual**:
    Asegúrate de tener un entorno virtual activo:
    ```bash
    python -m venv venv
    venv\Scripts\activate   # En Windows
    pip install -r requirements.txt
    ```

2.  **Variables de Entorno (`.env`)**:
    Crea un archivo `.env` en la raíz con las siguientes claves:
    ```ini
    ESIOS_TOKEN=tu_token_aqui
    DB_HOST=localhost
    DB_NAME=esios_db
    DB_USER=usuario
    DB_PASSWORD=password
    LOCAL_STORAGE_PATH=./local_data
    ```

## Flujo de Datos

1.  **Descarga**: El módulo `esios.downloader` consulta la API de ESIOS.
2.  **Almacenamiento**: Los ficheros crudos (ZIP, XML, JSON) se guardan organizadamente en `local_data` (o bucket configurado) mediante `src.storage`.
3.  **Procesamiento**: Módulos en `src.processors` leen los ficheros descargados para extraer información relevante.
4.  **Base de Datos**: La información procesada se inserta en la base de datos PostgreSQL mediante `src.db`.

## Notas Legales
Los datos descargados pertenecen a ESIOS/REE. Asegúrate de cumplir con sus términos de uso.
