
# Schema definitions for Liquicomun PRDV files
# These match the PHYSICAL structure of the CSV files.
# Metadata like 'periodo', 'liquidacion', and 'source_file' are added during processing.

LIQUICOMUN_SCHEMA = {
    'liq_prdvbaqh': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'precio_eur_mwh': 'NUMERIC(18,3)',
    },
    'liq_prdvdatos': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'frr_subir_mwh': 'NUMERIC(18,3)',
        'frr_bajar_mwh': 'NUMERIC(18,3)',
        'rr_subir_mwh': 'NUMERIC(18,3)',
        'rr_bajar_mwh': 'NUMERIC(18,3)',
        'desvio_sistema_mwh': 'NUMERIC(18,3)',
        'pbalsub_euros_mwh': 'NUMERIC(18,3)',
        'pbalbaj_euros_mwh': 'NUMERIC(18,3)',
        'perc_frr_min_s_frr_may': 'NUMERIC(18,3)',
        'precio_unico_dual': 'TEXT',
        'precio_dual_desv_subir_euros_mwh': 'NUMERIC(18,3)',
        'precio_dual_desv_bajar_euros_mwh': 'NUMERIC(18,3)',
        'precio_unico_desv_euros_mwh': 'NUMERIC(18,3)',
    },
    'liq_prdvsuqh': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'precio_eur_mwh': 'NUMERIC(18,3)',
    },
    'liq_enrrqhba': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_enrrqhsu': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_enrttrba': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_enrttrsu': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_ensecqhba': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_ensecqhsu': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_enterqhba': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    },
    'liq_enterqhsu': {
        'fecha': 'DATE',
        'hora': 'INTEGER',
        'qh': 'INTEGER',
        'cantidad_mwh': 'NUMERIC(18,3)',
    }
}
