
# Proyecto de Datos Energía (OMIE/ESIOS)

Plataforma de ingeniería de datos para la descarga, procesamiento y análisis del Mercado Eléctrico Ibérico.

## 📚 Documentación
Toda la documentación detallada se encuentra en la carpeta `docs/`:

1.  **[Arquitectura](docs/ARCHITECTURE.md)**: Visión general del diseño, flujo de datos y diagrama de componentes.
2.  **[Instalación y Setup](docs/SETUP.md)**: Guía paso a paso para desplegar con Docker o en local.
3.  **[Referencia API](docs/API_REFERENCE.md)**: Detalles técnicos sobre tablas de BBDD, DAGs de Airflow y estructura del código.
4.  **[Migración al Cloud](documentation/CLOUD_MIGRATION.md)**: Estrategia para mover el proyecto a Google Cloud Platform (GCP).
5.  **[Costes Cloud](documentation/CLOUD_COSTS_ES.md)**: Estimación de costes en GCP.

## 🚀 Inicio Rápido con Docker

```bash
docker-compose up -d
```
Accede a Airflow en [http://localhost:8080](http://localhost:8080).

## 🛠 Estado del Proyecto
*   ✅ **OMIE Marginal Prices**: Automatizado.
*   ✅ **OMIE Trades**: Automatizado y separado en su propio Pipeline diaria.
*   🚧 **ESIOS**: En desarrollo.
