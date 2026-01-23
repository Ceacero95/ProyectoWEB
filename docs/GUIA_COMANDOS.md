# Guía de Comandos (Airflow y GitHub)

Este documento contiene los comandos principales para gestionar el entorno de Airflow y sincronizar los cambios con GitHub.

## 1. Gestión de Airflow (Docker)

### Iniciar el entorno
```powershell
docker compose up -d
```
*   **Qué hace:** Levanta los contenedores (PostgreSQL, Webserver, Scheduler) en segundo plano.

### Detener el entorno
```powershell
docker compose down
```
*   **Qué hace:** Detiene y elimina los contenedores. Los datos de la base de datos persisten.

### Ver estado y logs
*   **Estado:** `docker compose ps`
*   **Logs:** `docker compose logs -f` (Ctrl+C para salir).

---

## 2. Gestión de GitHub

Para subir tus cambios al repositorio, usa estos tres comandos en orden:

### Paso 1: Preparar los archivos
```powershell
git add .
```
*   **Qué hace:** Indica a Git que quieres incluir todos los cambios realizados en la carpeta actual.

### Paso 2: Confirmar los cambios
```powershell
git commit -m "Descripción de lo que has hecho"
```
*   **Qué hace:** Crea un "punto de guardado" local con un mensaje descriptivo.

### Paso 3: Subir a la nube
```powershell
git push
```
*   **Qué hace:** Envía tus commits locales al repositorio de GitHub.

---

## Acceso Rápido
*   **Panel Airflow:** [http://localhost:8080](http://localhost:8080) (`admin` / `admin`)
*   **Ejecución Manual:** Todos los procesos están configurados como **manuales**. Para lanzar uno:
    1. Entra en el panel de Airflow.
    2. Busca el DAG (ej: `omie_pipeline`).
    3. Haz clic en el botón de "Play" (Trigger DAG) arriba a la derecha.
    4. Si quieres elegir fechas específicas, selecciona **"Trigger DAG w/ config"** y pasa un JSON:
       ```json
       {"start_date": "2025-01-01", "end_date": "2025-01-10"}
       ```
*   **Actualizar Código:** Si has descargado cambios de otros: `git pull`

## Troubleshooting

Si los DAGs no cargan:
1. Revisa `docker compose ps` (deben estar "Running" o "Up").
2. Mira los logs: `docker compose logs airflow-scheduler`.
