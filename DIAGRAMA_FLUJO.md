# 🗺️ Diagrama de Flujo y Arquitectura - ProyectoWEB

Este esquema visualiza cómo fluye la información a través de los diferentes módulos del sistema y cómo interactúan las piezas clave.

```mermaid
graph TD
    %% Estilos
    classDef entry fill:#f96,stroke:#333,stroke-width:2px;
    classDef logic fill:#9cf,stroke:#333,stroke-width:2px;
    classDef storage fill:#fd9,stroke:#333,stroke-width:2px;
    classDef external fill:#ddd,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;

    %% Nodos Externos
    User((Usuario))
    ESIOS[("☁️ API ESIOS (Ree.es)")]:::external
    AdminDB[("🗄️ PostgreSQL")]:::external
    GCS[("☁️ Google Cloud Storage")]:::external
    FileSystem[("📂 Sistema Archivos Local")]:::storage

    %% Entry Point
    subgraph CLI ["🖥️ Interfaz de Comandos (manage.py)"]
        Manage[manage.py]:::entry
    end

    %% Flujo 1: Descarga y Almacenamiento (Backfill)
    subgraph Downloader ["📥 Módulo de Descarga (src/esios)"]
        Backfill[downloader.py <br/> (Orquestador)]:::logic
        Client[client.py <br/> (Cliente HTTP)]:::logic
    end

    subgraph Storage ["💾 Gestión de Archivos (src/storage)"]
        Handler[handler.py <br/> (Abstracción Local/Nube)]:::logic
    end

    %% Flujo 2: Procesamiento (Nueva Arquitectura)
    subgraph Processors ["⚙️ Procesadores (src/processors)"]
        BaseProc[base.py <br/> (Clase Base)]:::logic
        I90Proc[i90.py]:::logic
        NewProc[...futuros... <br/> (i3.py, liquicomun.py)]:::logic
    end

    %% Flujo 3: API Server
    subgraph API ["🚀 Servidor API (src/api)"]
        MainAPI[main.py]:::logic
    end
    
    subgraph DB ["🔌 Base de Datos (src/db)"]
        CheckDB[connector.py]:::logic
    end

    %% Relaciones / Flujos
    User -- "1. python manage.py backfill" --> Manage
    User -- "2. python manage.py server" --> Manage

    %% Flujo Backfill
    Manage -- "Llama a" --> Backfill
    Backfill -- "Solicita datos" --> Client
    Client -- "HTTP GET" --> ESIOS
    Client -- "Retorna ZIP bytes" --> Backfill
    Backfill -- "Pasa datos a" --> Handler
    
    Handler -- "Guarda (Modo Local)" --> FileSystem
    Handler -- "Guarda (Modo GCP)" --> GCS
    
    %% Flujo Futuro de Procesamiento (Conceptual)
    FileSystem -.-> |"Lee archivos raw"| BaseProc
    BaseProc --> I90Proc
    I90Proc --> CheckDB
    CheckDB --> AdminDB

    %% Flujo API
    Manage -- "Inicia Uvicorn" --> MainAPI
    MainAPI -- "Consulta datos" --> CheckDB
    CheckDB -- "SQL Query" --> AdminDB
    MainAPI -- "JSON Response" --> User

```

## 📖 Diccionario de Componentes

### 1. **Entry Point (`manage.py`)**
Es el "cerebro" administrativo. No contiene lógica compleja, simplemente lee tus comandos (ej. `backfill`, `server`) y decide qué módulo activar.
*   *Modificado recién*: Ahora acepta `--name` para saber si descargas `i90`, `liquicomun`, etc.

### 2. **Módulo de Descarga (`src/esios`)**
*   **`downloader.py`**: El jefe de obra. Coordina las fechas, itera día a día y llama a los trabajadores.
*   **`client.py`**: El mensajero. Solo sabe cómo hacer peticiones a ESIOS y devolverte el paquete cerrado (ZIP).

### 3. **Gestión de Almacenamiento (`src/storage`)**
*   **`handler.py`**: El almacenero inteligente.
    *   Si estás en tu PC: Guarda en carpetas `raw/nombre_dataset/zips`.
    *   Si estás en la nube (GCP): Sube directamente al Bucket.
    *   *Ventaja*: El resto del programa no necesita saber dónde se guardan las cosas, solo le da el archivo al Handler.

### 4. **Procesadores (`src/processors`)** *(Nueva Capa)*
Aquí es donde ocurre la "magia" de los datos.
*   **`base.py`**: Define las reglas comunes (ej. "todos los procesadores deben tener una función `process_file`").
*   **`i90.py`**: El especialista en archivos i90. Aquí escribirás la lógica para leer el XML/CSV específico de i90 y limpiarlo.
*   Esta estructura te permite añadir `liquicomun.py` mañana sin romper nada de lo anterior.

### 5. **Base de Datos (`src/db`)**
*   **`connector.py`**: Tu enchuge a PostgreSQL. Maneja conexiones seguras y transacciones.
