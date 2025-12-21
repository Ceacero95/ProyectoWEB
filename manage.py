import argparse
import uvicorn
import os
import sys
from datetime import datetime

# Añadir directorio actual al path
sys.path.append(os.getcwd())

from src.esios.downloader import run_daily_sync, backfill_archive
from src.config import settings

def run_server(args):
    """Inicia el servidor API."""
    print("Iniciando servidor API...")
    uvicorn.run("src.api.main:app", host=args.host, port=args.port, reload=args.reload)

def run_sync(args):
    """Ejecuta la sincronización diaria de I3 y Liquicomun."""
    start = args.start_date or str(settings.I90_BACKFILL_START_DATE) # Default from settings if not provided
    run_daily_sync(start, args.end_date)

def run_backfill(args):
    """Ejecuta un backfill específico por ID."""
    if not args.archive_id or not args.name:
         print("ERROR: Para backfill manual se requiere --archive-id y --name.")
         return
    
    backfill_archive(args.archive_id, args.name, args.start_date, args.end_date)

def main():
    parser = argparse.ArgumentParser(description="Herramienta de gestión para ProyectoWEB")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Comando: server
    parser_server = subparsers.add_parser("server", help="Inicia el servidor API")
    parser_server.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser_server.add_argument("--port", type=int, default=8000, help="Puerto (default: 8000)")
    parser_server.add_argument("--reload", action="store_true", help="Activar auto-reload")
    parser_server.set_defaults(func=run_server)

    # Comando: sync (Nueva funcionalidad principal)
    parser_sync = subparsers.add_parser("sync", help="Descarga sistemática de I3 y Liquicomun (IDs configurados)")
    parser_sync.add_argument("--start-date", help="Fecha inicio YYYY-MM-DD (Opcional, default: settings)")
    parser_sync.add_argument("--end-date", help="Fecha fin YYYY-MM-DD (Default: hoy)")
    parser_sync.set_defaults(func=run_sync)

    # Comando: backfill (Manual)
    parser_backfill = subparsers.add_parser("backfill", help="Descarga manual de un ID específico")
    parser_backfill.add_argument("--archive-id", type=int, required=True, help="ID del archivo ESIOS")
    parser_backfill.add_argument("--name", type=str, required=True, help="Nombre del dataset (ej: otros)")
    parser_backfill.add_argument("--start-date", required=True, help="Fecha inicio YYYY-MM-DD")
    parser_backfill.add_argument("--end-date", help="Fecha fin YYYY-MM-DD")
    parser_backfill.set_defaults(func=run_backfill)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
