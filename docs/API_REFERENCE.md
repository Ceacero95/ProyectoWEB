
# Referencia de API y Base de Datos

## Base de Datos (PostgreSQL)
Esquema principal: `omie`.

### Tablas
#### 1. `omie.trades`
Almacena las transacciones casadas en el mercado intradiario continuo.
*   **Clave Primaria**: `(fecha, contrato, agente_compra, unidad_compra, agente_venta, unidad_venta, precio, cantidad, momento_casacion)`
*   **Columnas Clave**:
    *   `fecha`: Fecha de la transacción.
    *   `contrato`: Identificador del contrato (e.g., PH).
    *   `precio`: Precio en EUR/MWh.
    *   `cantidad`: Energía en MWh.
    *   `agente_*`: Identificadores de los agentes participantes.

#### 2. `omie.marginalpdbc`
Precios marginales del mercado diario (Portugués, pero aplicable a MIBEL bajo condiciones de Market Splitting).
*   **Clave Primaria**: `(fecha, periodo)` (aproximada).

## Airflow DAGs

### 1. `omie_pipeline` (`dags/omie_dag.py`)
*   **Propósito**: Descarga diaria de precios marginales y finales.
*   **Schedule**: 08:30 UTC.
*   **Tareas**:
    *   `download_pdbc` -> `process_pdbc`
    *   `download_marginal_pdbc` -> `process_marginal_pdbc`
    *   ... (y otros ficheros similares)

### 2. `trades_pipeline` (`dags/trades_dag.py`)
*   **Propósito**: Descarga de ficheros de Trades (Gran volumen).
*   **Schedule**: 10:00 UTC.
*   **Tareas**:
    *   `download_trades`: Descarga ZIP mensual.
    *   `process_trades`: Parsea el día correspondiente del ZIP.

## Estructura de Código (`src/`)

### `src/common`
*   `DatabaseManager`: Singleton para conexiones SQL y `bulk_insert_df` (COPY).
*   `StorageManager`: Abstracción de sistema de ficheros.
*   `OmieClient`: Cliente HTTP especializado para OMIE.

### `src/bronze`
Scripts que orquestan la descarga. No transforman datos, solo guardan ficheros raw.

### `src/silver`
Procesadores ETL.
*   Lectura de raw bytes.
*   Limpieza con Pandas.
*   Inserción idempotente en BBDD.
