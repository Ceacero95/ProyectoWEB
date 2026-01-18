# Cloud Integration Guide ☁️

This document outlines the strategy to deploy the **Energy Data Ecosystem** to the three major cloud providers: **AWS**, **Azure**, and **Google Cloud Platform (GCP)**.

Since the project is **Containerized (Docker)** and uses **Environment Variables** for configuration, migration is straightforward.

---

## 🏗️ General Architecture Mapping

| Component | Local (Current) | AWS | Azure | GCP |
| :--- | :--- | :--- | :--- | :--- |
| **Orchestrator** | Docker Airflow | **MWAA** (Managed Airflow) or **ECS Fargate** | **Azure Data Factory** (pipelines) or **AKS/ACI** | **Cloud Composer** or **Cloud Run** |
| **Database** | Postgres Container | **Amazon RDS** for PostgreSQL | **Azure Database** for PostgreSQL | **Cloud SQL** for PostgreSQL |
| **Analytics DB** | Postgres (Gold) | **Redshift** or **Athena** | **Synapse Analytics** | **BigQuery** |
| **Storage** | Local Volume | **S3** Bucket | **Blob Storage** | **Cloud Storage (GCS)** |

---

## 1. Google Cloud Platform (GCP) - *Recommended*

GCP is the most natural fit due to its strong data/analytics focus (BigQuery) and native Airflow support (Cloud Composer).

### Steps:
1.  **Storage (GCS)**:
    - Create a bucket `gs://energy-data-lake`.
    - Update code to use `google-cloud-storage` client instead of local file system (requires minor code tweak in `StorageManager`).
2.  **Database (BigQuery)**:
    - The "Gold" layer is best served by **BigQuery**. Update `DatabaseManager` to load DataFrames to BigQuery tables.
3.  **Compute (Cloud Run / Composer)**:
    - **Option A (Cheapest)**: Deploy the Docker image to **Cloud Run Jobs**. Trigger it with Cloud Scheduler.
    - **Option B (Native)**: Use **Cloud Composer**. It's a managed Airflow environment. You just upload your `dags/` folder to the DAGs bucket.
4.  **Configuration**:
    - Set `DATABASE_URL` to point to Cloud SQL or BigQuery connection string.

---

## 2. Amazon Web Services (AWS)

### Steps:
1.  **Storage (S3)**:
    - Create an S3 bucket.
    - Update `StorageManager` to use `boto3`.
2.  **Database (RDS)**:
    - Provision an **RDS for PostgreSQL** instance.
    - Update the `DATABASE_URL` env var.
3.  **Compute (ECS Fargate)**:
    - Push your Docker image to **ECR (Elastic Container Registry)**.
    - Create an **ECS Task Definition** pointing to the image.
    - Schedule the task using **EventBridge**.
    *Alternatively, use **MWAA** (Managed Workflows for Apache Airflow) and upload your DAGs to S3.*

---

## 3. Microsoft Azure

### Steps:
1.  **Storage (Blob Storage)**:
    - Create a Storage Account container.
    - Update `StorageManager` to use `azure-storage-blob`.
2.  **Database (Azure SQL)**:
    - Use **Azure Database for PostgreSQL**.
    - Configure connection strings in `config/settings.py`.
3.  **Compute (ACI / AKS)**:
    - Push image to **Azure Container Registry (ACR)**.
    - Deploy to **Azure Container Instances (ACI)** for simple execution or **AKS** for full orchestration.

---

## 🔑 Key Code Adaptations Required

To ensure 100% cloud compatibility, one specific change is recommended in `src/common/filesystem.py`:

**Abstract the File System**:
Currently, `StorageManager` writes to disk.
- **Refactor**: Create an interface `IStorage` with `read()`, `write()`, `exists()`.
- **Implementations**: `LocalStorage`, `S3Storage`, `GCSStorage`, `AzureBlobStorage`.
- **Switch**: Select implementation based on an env var `STORAGE_BACKEND`.


---

## 4. 🚀 Phase 1: Hybrid Integration (Local Compute + GCP Data)

This is the most cost-effective starting point. You run Airflow on your local machine (Docker) but store all valuable data in the cloud.

### Step-by-Step Implementation

1.  **GCP Setup**:
    *   Create a Project in Google Cloud Console.
    *   Enable **BigQuery API** and **Google Cloud Storage API**.
    *   Create a **Service Account** with roles: `BigQuery Admin` and `Storage Admin`.
    *   Download the **JSON Key** for this account. Save it as `gcp_credentials.json` in your local project root.

2.  **Configuration (Docker)**:
    *   Move `gcp_credentials.json` to a folder mounted in Docker (e.g., inside `local_data/`).
    *   Update `.env` or `docker-compose.yaml` with:
        ```yaml
        GOOGLE_APPLICATION_CREDENTIALS: /opt/airflow/local_data/gcp_credentials.json
        GCP_PROJECT_ID: your-project-id
        STORAGE_BACKEND: GCS  # Feature toggle we must implement
        ```

3.  **Code Changes Needed**:
    *   **StorageManager**: Add logic to check `STORAGE_BACKEND`. If 'GCS', use `from google.cloud import storage`.
    *   **DatabaseManager**: Add logic to check `DATABASE_URL`. If it starts with `bigquery://`, use `pandas_gbq` or `sqlalchemy-bigquery`.


---

## 5. 🗄️ Database Strategy: Cloud SQL vs BigQuery

For this specific project (Energy Data Analytics), strictly using **Cloud SQL (PostgreSQL)** is **NOT recommended** if you want to optimize costs and performance.

### Comparison

| Feature | Cloud SQL (PostgreSQL) | BigQuery (Recommended) |
| :--- | :--- | :--- |
| **Type** | Transactional (OLTP) | Analytical (OLAP) |
| **Cost** | **~15-30 €/month** (Instance running 24/7) | **~0 €/month** (Pay per query/storage, Free Tier includes 10GB & 1TB queries) |
| **Scaling** | Manual resizing (Vertical) | Serverless / Infinite (Horizontal) |
| **Best For** | User sessions, Shopping carts, complex joins | **Millions of rows**, Aggregations, Reporting, Dashboards |
| **Maintenance**| Tunings, Updates, Backups | Zero maintenance |

### Recommendation
Use **BigQuery** as your "Gold Layer".
1.  **Cost**: It fits perfectly in the Free Tier.
2.  **Performance**: Querying millions of energy records (e.g., historical prices) is instant.
3.  **Integration**: Native integration with Google Data Studio (Looker) for dashboards.

*Note: If you need a small transactional DB for Airflow metadata (users, run history) in the cloud, a tiny Postgres instance is required, but Airflow itself can run on a simple SQLite for low-volume personal projects, or you can use Heroku Postgres (Free/Cheap) just for the metadata.*


