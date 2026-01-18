# Datos para la Calculadora de Precios GCP 🧮

Este documento contiene los datos métricos exactos de tu proyecto actual para que los introduzcas en la [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator).

---

## 1. Almacenamiento (Google Cloud Storage)
*Clase: Standard Storage (Europe-SouthWest1)*

| Métrica | Valor Actual | Estimación a 1 Año | Notas |
| :--- | :--- | :--- | :--- |
| **Volumen Inicial** | **2.5 GB** (Aprox) | **5 GB** | Basado en históricos de ESIOS/OMIE (2019-2026). |
| **Operaciones A** | ~500 ops/mes | ~1000 ops/mes | Subidas diarias (PUT) de nuevos ficheros. |
| **Operaciones B** | ~2000 ops/mes | ~5000 ops/mes | Descargas de Airflow para procesar. |
| **Network Egress** | < 1 GB/mes | < 1 GB/mes | Salida de datos (si descargas a tu PC). |

---

## 2. Base de Datos Analítica (BigQuery)
*Región: Europe-SouthWest1 (Madrid)*

| Métrica | Valor Actual | Estimación a 1 Año | Notas |
| :--- | :--- | :--- | :--- |
| **Active Storage** | **1.2 GB** | **3 GB** | Tamaño comprimido en columna. |
| **Streaming Inserts** | 0 MB | 0 MB | Usamos "Batch Loads" (Gratis). |
| **Query Data Processed** | ~10 GB/mes | ~50 GB/mes | Depende de cuántas consultas hagas. El Free Tier regala 1000 GB/mes. |

---

## 3. Computación (Cloud Run Jobs) - *Opción Serverless*
*Configuración: 1 vCPU, 2 GB RAM (Tier 1)*

| Métrica | Input Calculadora | Notas |
| :--- | :--- | :--- |
| **Número de Jobs** | 1 | Ejecución diaria. |
| **Ejecuciones/mes** | 30 | Una vez al día. |
| **Duración/Job** | 900 segundos (15 min) | Tiempo promedio de descarga+proceso. |
| **vCPU Requests** | 1 | |
| **Memory Requests** | 2 GB | |

**Resultado Esperado**: 0,00 € (Totalmente cubierto por Free Tier).

---

## 4. Base de Datos Transaccional (Cloud SQL) - *OPCIONAL*
*Solo si decides NO usar la opción BigQuery pura y quieres un Postgres real.*

*   **Instance Type**: `db-f1-micro` (Shared Core)
*   **Storage**: 10 GB SSD.
*   **High Availability**: No.
*   **Backups**: Automated daily.

**Resultado Esperado**: ~15,00 € / mes.

---

## Resumen para la Calculadora
Al rellenar, selecciona siempre la región **Madrid (europe-southwest1)** o **Belgium (europe-west1)** (a veces más barata).

*   **GCS**: 5 GB.
*   **BigQuery**: 2 GB Storage, 10 GB Queries.
*   **Cloud Run**: 1 vCPU, 2GB RAM, 7.5 horas/mes.
