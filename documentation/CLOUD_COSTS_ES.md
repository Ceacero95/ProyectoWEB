# Cloud Cost Estimation (Spain) 💶

**Scenario**: 24/7 Execution of Airflow Webserver/Scheduler + Managed Database.
**Resource Profile**: "Small Production"
- **Compute**: 2 vCPU, 4 GB RAM (Total for Airflow components).
- **Database**: Managed PostgreSQL (1 vCPU, 2-4GB RAM, 20GB Storage).
- **Object Storage**: 50 GB Standard.

---

## 1. Google Cloud Platform (Region: `europe-southwest1` - Madrid)

GCP offers the most granular billing (per second) and strict integration with BigQuery.

| Service | SKU / Config | Monthly Cost (Approx) |
| :--- | :--- | :--- |
| **Compute** | **Cloud Run** (always on CPU, 2 vCPU, 4GB) or **e2-medium** VM | ~55 € |
| **Database** | **Cloud SQL** (Micro instance, shared vCPU) | ~15 € |
| **Analytics** | **BigQuery** (Storage + Queries) | < 1 € (Free Tier usually covers this size) |
| **Storage** | **GCS** (50GB Standard) | ~1 € |
| **Total** | | **~71 € / mes** |

*Note: If you use "Cloud Composer" (Managed Airflow), the base cost is ~300€/month. We assume "Self-Hosted on Cloud Run/Compute Engine" for this estimate.*

---

## 2. Amazon Web Services (Region: `eu-south-2` - Spain)

AWS Spain region tends to be slightly more expensive than Ireland/Frankfurt.

| Service | SKU / Config | Monthly Cost (Approx) |
| :--- | :--- | :--- |
| **Compute** | **ECS Fargate** (2 vCPU, 4GB RAM, 730h) | ~65 € |
| **Database** | **RDS PostgreSQL** (db.t4g.micro, 20GB) | ~18 € |
| **Storage** | **S3** (50GB Standard) | ~1.20 € |
| **Total** | | **~84.20 € / mes** |

---

## 3. Microsoft Azure (Region: `Spain Central` - Madrid)

| Service | SKU / Config | Monthly Cost (Approx) |
| :--- | :--- | :--- |
| **Compute** | **Azure Container Instances** (2 vCPU, 4GB) | ~90 € (ACI is expensive for 24/7) |
| **Alt. Compute** | **B2s VM** (Linux, 2vCPU, 4GB) | ~35 € (Much cheaper option) |
| **Database** | **Azure Database for PostgreSQL** (Burstable B1ms) | ~25 € |
| **Storage** | **Blob Storage** (Hot, 50GB) | ~1 € |
| **Total** | **(Using VM)** | **~61 € / mes** |

---

## 🏆 Verdict for Low Cost

1.  **Azure (VM B-Series)**: **~61 €** (Best value for always-on VM compute in Spain).
2.  **GCP (Cloud Run/e2)**: **~71 €** (Best for integration with BigQuery and Modern stack).
3.  **AWS**: **~84 €** (Fargate is convenient but costs add up).


---

## 4. 💡 La Opción "Hacker" (Capa Gratuita / Low Cost)

Para conseguir coste **Casi Cero (0 €)**, debemos abandonar la idea de tener un servidor "encendido 24/7" (Airflow Scheduler) y pasar a un modelo **Serverless** (Ejecución por lotes).

### Arquitectura Propuesta (GCP Free Tier)

1.  **Orquestador**: Eliminar Airflow. Usar **Google Cloud Scheduler** (0.10€/mes o Gratis 3 jobs).
2.  **Computación**: **Google Cloud Run Jobs**.
    *   Dockerizas tu script `esios_dag.py` para que en vez de un DAG, sea un script lineal `main.py`.
    *   Se despierta 1 vez al día, procesa 20 min y se apaga.
    *   **Coste**: Gratis (La capa gratuita incluye 50 vCPU-horas/mes. Si tu proceso tarda < 1.5h al día, es gratis).
3.  **Base de Datos**: **Google BigQuery**.
    *   **Almacenamiento**: 10 GB Gratis (suficiente para varios años de este proyecto).
    *   **Consultas**: 1 TB/mes Gratis.
4.  **Almacenamiento Ficheros**: **Google Cloud Storage**.
    *   5 GB Gratis (solo en regiones US-WEST1/CENTRAL1/EAST1). En Europa cuesta céntimos.

### Resumen del Plan Gratis (Serverless)

| Componente | Servicio | Coste Estimado |
| :--- | :--- | :--- |
| **Scheduler** | Cloud Scheduler | 0 € |
| **Compute** | Cloud Run Jobs | 0 € (dentro de límites) |
| **Database** | BigQuery | 0 € |
| **Storage** | GCS (Europe) | ~0.20 € |
| **TOTAL** | | **< 1 € / mes** |

**Trade-off**: Pierdes la UI gráfica de Airflow y la capacidad de reintentos complejos (hay que programarlo en Python), pero ahorras ~70€/mes.

