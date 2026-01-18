
# Manual de Configuración y Despliegue

## Requisitos Previos
*   **Docker** y **Docker Compose** instalados.
*   o **Python 3.9+** y **PostgreSQL** local (para ejecución sin Docker).

## 1. Ejecución con Docker (Recomendado)
Este método levanta Airflow, PostgreSQL y todos los servicios necesarios automáticamente.

1.  **Clonar el repositorio**:
    ```bash
    git clone <repo-url>
    cd ProyectoWEB
    ```

2.  **Configurar Variables de Entorno**:
    Crea un fichero `.env` en la raíz (usa `.env.example` como guía).
    ```ini
    POSTGRES_USER=airflow
    POSTGRES_PASSWORD=airflow
    POSTGRES_DB=airflow
    DATABASE_URL=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
    ```

3.  **Iniciar Servicios**:
    ```bash
    docker-compose up -d
    ```

4.  **Acceder a la Interfaz**:
    *   Airflow UI: `http://localhost:8080` (User/Pass: `airflow`/`airflow`)

## 2. Ejecución Local (Desarrollo)
Si quieres ejecutar scripts individuales sin Airflow:

1.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar DB Local**:
    Asegúrate de tener un PostgreSQL corriendo y actualiza `DATABASE_URL` en `.env` para apuntar a `localhost`.

3.  **Ejecutar módulos**:
    ```bash
    # Ejemplo: Descargar Trades de 2025
    python backfill_trades_2025.py
    ```

## 3. Estructura de Carpetas
*   `dags/`: Definiciones de workflows de Airflow.
*   `src/`: Código fuente Python.
*   `local_data/`: Almacenamiento local de ficheros Bronze/Silver (ignorado por Git).
*   `docs/`: Documentación del proyecto.
