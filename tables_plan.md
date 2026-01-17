# Proposed Liquicomun Tables

### Table: `liq_2025`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| 18 | TEXT | 18 |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_afrrbaj`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_afrrsub`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_bamerupg`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| periodo | TIMESTAMP | Periodo |
| upg_ventas_md | NUMERIC(18,3) | UPG ventas MD |
| upg_ventas_mi | NUMERIC(18,3) | UPG ventas MI |
| upg_ventas_cbm | NUMERIC(18,3) | UPG ventas CBM |
| upg_ventas_saj | NUMERIC(18,3) | UPG ventas SAJ |
| upg_compras_md | NUMERIC(18,3) | UPG compras MD |
| upg_compras_mi | NUMERIC(18,3) | UPG compras MI |
| upg_compras_cbm | NUMERIC(18,3) | UPG compras CBM |
| upg_compras_saj | NUMERIC(18,3) | UPG compras SAJ |
| upg_ventas_total | NUMERIC(18,3) | UPG ventas total |
| upg_compras_total | NUMERIC(18,3) | UPG compras total |
| balance_upg | NUMERIC(18,3) | Balance UPG |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_baprdeme`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| actividad | TEXT | Actividad |
| energia_*_producida_y_consumida__mwh | NUMERIC(18,3) | Energía (*) producida y consumida  MWh |
| cuota_sobre_produccion_y_consumo_% | NUMERIC(18,1) | Cuota sobre producción y consumo % |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_baprodem`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| periodo | TIMESTAMP | Período |
| ro_nuclear | NUMERIC(18,3) | RO Nuclear |
| ro_carbon | NUMERIC(18,3) | RO Carbón |
| ro_cc_gas | NUMERIC(18,3) | RO CC Gas |
| ro_cogen | NUMERIC(18,3) | RO Cogen |
| ro_fuel-gas | NUMERIC(18,3) | RO Fuel-gas |
| ro_hidraulico | NUMERIC(18,3) | RO Hidráulico |
| ro_genbomb | NUMERIC(18,3) | RO GenBomb |
| ro_conbomb | NUMERIC(18,3) | RO ConBomb |
| re_termico | NUMERIC(18,3) | RE Térmico |
| re_hidraulico | NUMERIC(18,3) | RE Hidráulico |
| re_eolico | NUMERIC(18,3) | RE Eólico |
| re_solar | NUMERIC(18,3) | RE Solar |
| importacion | NUMERIC(18,3) | Importación |
| consumo_con_cur | NUMERIC(18,3) | Consumo con CUR |
| consumo_sin_cur | NUMERIC(18,3) | Consumo sin CUR |
| exportacion | NUMERIC(18,3) | Exportación |
| ro+re_+import | NUMERIC(18,3) | RO+RE +IMPORT |
| demanda+cie_+exp+_enlace | NUMERIC(18,3) | DEMANDA+CIE +EXP+ ENLACE |
| balance | NUMERIC(18,3) | Balance |
| cierre_energia | NUMERIC(18,3) | Cierre energía |
| enlace_baleares | NUMERIC(18,3) | Enlace Baleares |
| re_aux | NUMERIC(18,3) | RE Aux |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_caleliqui`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| ano | INTEGER | Año |
| mes | INTEGER | Mes |
| facturacion | INTEGER | Facturación |
| fecha_avance_fecha_limite_para_facturaciones_3,_4_y_5 | DATE | Fecha avance (Fecha límite para facturaciones 3, 4 y 5) |
| fecha_reclamaciones | DATE | Fecha reclamaciones |
| fecha_cierre | DATE | Fecha cierre |
| fecha_emision_factura | DATE | Fecha emisión factura |
| fecha_cobros_y_pagos | DATE | Fecha cobros y pagos |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_cilraipre`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| cil | TEXT | CIL |
| raipre | TEXT | RAIPRE |
| potencia_mw | NUMERIC(18,2) | Potencia MW |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_clhqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| coeficiente | NUMERIC(18,5) | COEFICIENTE |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_codsvbaqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_codsvsuqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_compodem`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia | DATE | Día |
| hora | INTEGER | Hora |
| segmento | TEXT | Segmento |
| tipo_demanda | TEXT | Tipo demanda |
| coste_eur | NUMERIC(18,2) | Coste EUR |
| demanda_mwh_bc | NUMERIC(18,3) | Demanda MWh bc |
| coste_eur_mwh_bc | NUMERIC(18,10) | Coste EUR/MWh bc |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_comppfre`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| tecnologia | TEXT | Tecnología |
| produccion_medida_liquidada_mwh | NUMERIC(18,3) | Producción medida liquidada MWh |
| produccion_a_precio_mercado_diario_eur | NUMERIC(18,2) | Producción a precio mercado diario EUR |
| ganancia_perdida_intradiario_eur | NUMERIC(18,2) | Ganancia/Pérdida Intradiario EUR |
| ganancia_restricciones_tecnicas_eur | NUMERIC(18,2) | Ganancia restricciones técnicas EUR |
| perdida_por_coste_desvios_eur | NUMERIC(18,2) | Pérdida por coste desvíos EUR |
| perdida_por_coste_reserva_subir_eur | NUMERIC(18,2) | Pérdida por coste reserva subir EUR |
| precio_medio_a_mdiario_eur_mwh | NUMERIC(18,2) | Precio medio a m.diario EUR/MWh |
| ganancia_perdida_intradiario_eur_mwh | NUMERIC(18,2) | Ganancia/Pérdida Intradiario EUR/MWh |
| ganancia_restricciones_tecnicas_eur_mwh | NUMERIC(18,2) | Ganancia restricciones técnicas EUR/MWh |
| perdida_por_coste_desvios_eur_mwh | NUMERIC(18,2) | Pérdida por coste desvíos EUR/MWh |
| perdida_por_coste_reserva_subir_eur_mwh | NUMERIC(18,2) | Pérdida por coste reserva subir EUR/MWh |
| ingreso_total_mercado_eur_mwh | NUMERIC(18,2) | Ingreso total mercado EUR/MWh |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_cosdsvqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_cuotaadq`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| actividad | TEXT | Actividad |
| sujeto_de_liquidacion | TEXT | Sujeto de Liquidación |
| demanda_mwh_bc | NUMERIC(18,3) | Demanda MWh bc |
| cuota_sujeto_% | NUMERIC(18,4) | Cuota Sujeto % |
| cuota_acumulada_% | NUMERIC(18,1) | Cuota acumulada % |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_cuotafro`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| sujeto | TEXT | Sujeto |
| andorra_exportacion_mwh | INTEGER | Andorra exportación MWh |
| andorra_importacion_mwh | INTEGER | Andorra importación MWh |
| francia_exportacion_mwh | INTEGER | Francia exportación MWh |
| francia_importacion_mwh | INTEGER | Francia importación MWh |
| portugal_exportacion_mwh | INTEGER | Portugal exportación MWh |
| portugal_importacion_mwh | INTEGER | Portugal importación MWh |
| marruecos_exportacion_mwh | INTEGER | Marruecos exportación MWh |
| marruecos_importacion_mwh | INTEGER | Marruecos importación MWh |
| andorra_exportacion_% | NUMERIC(18,2) | Andorra exportación % |
| andorra_importacion_% | NUMERIC(18,2) | Andorra importación % |
| francia_exportacion_% | NUMERIC(18,2) | Francia exportación % |
| francia_importacion_% | NUMERIC(18,2) | Francia importación % |
| marruecos_exportacion_% | NUMERIC(18,2) | Marruecos exportación % |
| marruecos_importacion_% | NUMERIC(18,2) | Marruecos importación % |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_cuotaven`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| actividad | TEXT | Actividad |
| sujeto_de_liquidacion | TEXT | Sujeto de Liquidación |
| produccion_mwh_bc | NUMERIC(18,3) | Producción MWh bc |
| cuota_sujeto_% | NUMERIC(18,4) | Cuota Sujeto % |
| cuota_acumulada_% | NUMERIC(18,1) | Cuota acumulada % |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_diasinha`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dias_inhabiles_madrid_a_efectos_po_141,_66 | DATE | Días inhábiles Madrid a efectos PO 14.1, 6.6 |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enacbaqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endcodqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endcomqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endcurqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endexpqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endfrpoqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endimpqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endireqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endlibqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endreeoqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endrehiqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endretqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endronzqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endrozrqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endsvqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enduadqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endvbrpqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_endvlbqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enerad`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_eninqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_eninqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enitbqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enitbqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enpeboeqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enpeexqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enperdiqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enpertpqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enrepscqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enrrqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enrrqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enrttrba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enrttrsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_ensecqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_ensecqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enterqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_enterqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_festgppe`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| festivo_a_efectos_de_periodos_tarifarios | DATE | Festivo a efectos de periodos tarifarios |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_ficheliq`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fichero | TEXT | Fichero |
| sesion | INTEGER | Sesión |
| dia_1 | INTEGER | Día 1 |
| dia_2 | INTEGER | Día 2 |
| dia_3 | INTEGER | Día 3 |
| dia_4 | INTEGER | Día 4 |
| dia_5 | INTEGER | Día 5 |
| dia_6 | INTEGER | Día 6 |
| dia_7 | INTEGER | Día 7 |
| dia_8 | INTEGER | Día 8 |
| dia_9 | INTEGER | Día 9 |
| dia_10 | INTEGER | Día 10 |
| dia_11 | INTEGER | Día 11 |
| dia_12 | INTEGER | Día 12 |
| dia_13 | INTEGER | Día 13 |
| dia_14 | INTEGER | Día 14 |
| dia_15 | INTEGER | Día 15 |
| dia_16 | INTEGER | Día 16 |
| dia_17 | INTEGER | Día 17 |
| dia_18 | INTEGER | Día 18 |
| dia_19 | INTEGER | Día 19 |
| dia_20 | INTEGER | Día 20 |
| dia_21 | INTEGER | Día 21 |
| dia_22 | INTEGER | Día 22 |
| dia_23 | INTEGER | Día 23 |
| dia_24 | INTEGER | Día 24 |
| dia_25 | INTEGER | Día 25 |
| dia_26 | INTEGER | Día 26 |
| dia_27 | INTEGER | Día 27 |
| dia_28 | INTEGER | Día 28 |
| dia_29 | INTEGER | Día 29 |
| dia_30 | INTEGER | Día 30 |
| dia_31 | INTEGER | Día 31 |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_gaprdema`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| sistema_electrico | TEXT | Sistema eléctrico |
| precio_eur_mwh | NUMERIC(18,2) | Precio EUR/MWh |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_grdesvio`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia_y_hora | TIMESTAMP | Día y hora |
| zr_s | NUMERIC(18,2) | ZR s |
| zr_b | NUMERIC(18,2) | ZR b |
| ro_sin_zr_s | NUMERIC(18,2) | RO sin ZR s |
| ro_sin_zr_a_b | NUMERIC(18,2) | RO sin ZR a b |
| re_termico_s | NUMERIC(18,2) | RE Térmico s |
| re_termico_b | NUMERIC(18,2) | RE Térmico b |
| re_hidraulico_s | NUMERIC(18,2) | RE Hidráulico s |
| re_hidraulico_b | NUMERIC(18,2) | RE Hidráulico b |
| re_solar_s | NUMERIC(18,2) | RE Solar s |
| re_solar_b | NUMERIC(18,2) | RE Solar b |
| re_eolico_s | NUMERIC(18,2) | RE Eólico s |
| re_eolico_b | NUMERIC(18,2) | RE Eólico b |
| intercambio_internacional_s | NUMERIC(18,2) | Intercambio internacional s |
| intercambio_internacional_b | NUMERIC(18,2) | Intercambio internacional b |
| distribucion_s | NUMERIC(18,2) | Distribución s |
| distribucion_b | NUMERIC(18,2) | Distribución b |
| consumidor_directo_s | NUMERIC(18,2) | Consumidor directo s |
| consumidor_directo_b | NUMERIC(18,2) | Consumidor directo b |
| desvios_entre_sistemas_s | NUMERIC(18,2) | Desvíos entre sistemas s |
| desvios_entre_sistemas_b | NUMERIC(18,2) | Desvíos entre sistemas b |
| desvio_total | NUMERIC(18,2) | Desvío total |
| enlace_balear_subir | NUMERIC(18,2) | Enlace balear subir |
| enlace_balear_bajar | NUMERIC(18,2) | Enlace balear bajar |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_grpbfmed_`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia_y_hora | TIMESTAMP | Día y hora |
| energia_pbf | NUMERIC(18,2) | Energía PBF |
| energia_pvp | NUMERIC(18,2) | Energía PVP |
| energia_phf | NUMERIC(18,2) | Energía PHF |
| energia_p48 | NUMERIC(18,2) | Energía P48 |
| medida | NUMERIC(18,2) | Medida |
| energia_restricciones_pbf | NUMERIC(18,2) | Energía restricciones PBF |
| energia_mercado_intradiario | NUMERIC(18,2) | Energía mercado intradiario |
| energia_restricciones_tiempo_real | NUMERIC(18,2) | Energía restricciones tiempo real |
| desvio | NUMERIC(18,2) | Desvío |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_grpreolr`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia_hora | TIMESTAMP | Día hora |
| rcr_eolico_medido | NUMERIC(18,3) | RCR Eólico medido |
| rcr_eolico_programado | NUMERIC(18,3) | RCR Eólico programado |
| rcr_termico_no_renovable_medido | NUMERIC(18,3) | RCR Térmico no renovable medido |
| rcr_termico_no_renovable_programado | NUMERIC(18,3) | RCR Térmico no renovable programado |
| rcr_eolico_medida-programa | NUMERIC(18,3) | RCR Eólico medida-programa |
| rcr_termico_no_renovable_medida-programa | NUMERIC(18,3) | RCR Térmico no renovable medida-programa |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_grpresfh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia_hora | TEXT | Día hora |
| rcr_hidraulico_medido | NUMERIC(18,3) | RCR hidráulico medido |
| rcr_hidraulico_programado | NUMERIC(18,1) | RCR hidráulico programado |
| rcr_biogas_biomasa_medido | NUMERIC(18,3) | RCR biogas/biomasa medido |
| rcr_biogas_biomasa_programado | NUMERIC(18,1) | RCR biogas/biomasa programado |
| rcr_hidraulico_medida-programa | NUMERIC(18,3) | RCR hidráulico medida-programa |
| rcr_biogas_biomasa_medida-programa | NUMERIC(18,3) | RCR biogas/biomasa medida-programa |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_grpresol`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia_hora | TIMESTAMP | Día hora |
| termosolar_medido | NUMERIC(18,3) | Termosolar medido |
| termosolar_programa | NUMERIC(18,1) | Termosolar programa |
| fotovoltaico_medido | NUMERIC(18,3) | Fotovoltaico medido |
| fotovoltaico_programa | NUMERIC(18,1) | Fotovoltaico programa |
| termosolar_desvio | NUMERIC(18,3) | Termosolar desvío |
| fotovoltaico_desvio | NUMERIC(18,3) | Fotovoltaico desvío |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_iimpmcfpo`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| desde | DATE | DESDE |
| hasta | DATE | HASTA |
| importe | NUMERIC(18,2) | Importe |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_impdsvqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| importe_eur | NUMERIC(18,2) | IMPORTE (EUR) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_imresecqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| importe_eur | NUMERIC(18,2) | IMPORTE (EUR) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_imsecxqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| importe_eur | NUMERIC(18,2) | IMPORTE (EUR) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_inceinve`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| incentivo | TEXT | Incentivo |
| nº_instalaciones_autorizadas_el_ultimo_dia_del_mes | INTEGER | Nº instalaciones autorizadas el último día del mes |
| potencia_autorizada_el_ultimo_dia_del_mes_mw | INTEGER | Potencia autorizada el último día del mes MW |
| nº_instalaciones_que_reciben_incentivo | INTEGER | Nº instalaciones que reciben incentivo |
| potencia_incentivada_mw | INTEGER | Potencia incentivada MW |
| cantidad_recibida_eur | INTEGER | Cantidad recibida EUR |
| precio_eur_mw | INTEGER | Precio EUR/MW |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_indimes4`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| nombre_grupo | TEXT | Nombre grupo |
| fecha_dato | DATE | Fecha |
| codigo | TEXT | Código |
| version | INTEGER | Versión |
| desde | DATE | Desde |
| periodo_inicio | INTEGER | Período inicio |
| hasta | DATE | Hasta |
| periodo_fin | INTEGER | Período fin |
| potencia_indisponible_mw | NUMERIC(18,2) | Potencia indisponible MW |
| valor_de_etiqueta | INTEGER | Valor de etiqueta |
| comentario | TEXT | Comentario |
| fecha_registro | DATE | Fecha registro |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_itafrrba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_itafrrsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_kestimqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| coeficiente | NUMERIC(18,5) | COEFICIENTE |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_kestmedio`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| peaje | TEXT | Peaje |
| dia_1 | NUMERIC(18,2) | Día 1 |
| dia_2 | NUMERIC(18,2) | Día 2 |
| dia_3 | NUMERIC(18,2) | Día 3 |
| dia_4 | NUMERIC(18,2) | Día 4 |
| dia_5 | NUMERIC(18,2) | Día 5 |
| dia_6 | NUMERIC(18,2) | Día 6 |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_krealqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| coeficiente | NUMERIC(18,5) | COEFICIENTE |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_listfich`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| nombre_del_fichero | TEXT | Nombre del fichero |
| contenido | TEXT | Contenido |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_medbcdem`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| peaje | TEXT | Peaje |
| periodo_1 | NUMERIC(18,2) | Periodo 1 |
| periodo_2 | NUMERIC(18,2) | Periodo 2 |
| periodo_3 | NUMERIC(18,2) | Periodo 3 |
| periodo_4 | NUMERIC(18,2) | Periodo 4 |
| periodo_5 | NUMERIC(18,2) | Periodo 5 |
| periodo_6 | NUMERIC(18,2) | Periodo 6 |
| total | NUMERIC(18,2) | Total |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_mfrrdirsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_mfrrprosu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_modelcom1_v2-p1-a1_`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| formato | TEXT | Formato |
| fichero | TEXT | Fichero |
| contenido | TEXT | Contenido |
| periodo | TEXT | Periodo |
| desde | DATE | Desde |
| hasta | DATE | Hasta |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_modelcom3_v2-p2-a1_`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fichero | TEXT | Fichero |
| descripcion | TEXT | Descripción |
| periodo | TEXT | Periodo |
| sistema | TEXT | Sistema |
| desde | DATE | Desde |
| hasta | DATE | Hasta |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_modelcom4_v2-p2-a2`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fichero | TEXT | FICHERO |
| numero_de_orden_del_campo_en_el_fichero | INTEGER | NÚMERO DE ORDEN DEL CAMPO EN EL FICHERO |
| campo | TEXT | CAMPO |
| formato | TEXT | FORMATO |
| desde | TEXT | DESDE |
| hasta | DATE | HASTA |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_paraliq`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| codigo | TEXT | Código |
| desde | DATE | Desde |
| hasta | DATE | Hasta |
| valor | NUMERIC(18,5) | Valor |
| comentario | TEXT | Comentario |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pcaidema`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| peaje | TEXT | Peaje |
| periodo_1 | NUMERIC(18,2) | Periodo 1 |
| periodo_2 | NUMERIC(18,2) | Periodo 2 |
| periodo_3 | NUMERIC(18,2) | Periodo 3 |
| periodo_4 | NUMERIC(18,2) | Periodo 4 |
| periodo_5 | NUMERIC(18,2) | Periodo 5 |
| periodo_6 | NUMERIC(18,2) | Periodo 6 |
| total | NUMERIC(18,2) | Total |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pcardema`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| peaje | TEXT | Peaje |
| periodo_1 | NUMERIC(18,2) | Periodo 1 |
| periodo_2 | NUMERIC(18,2) | Periodo 2 |
| periodo_3 | NUMERIC(18,2) | Periodo 3 |
| periodo_4 | NUMERIC(18,2) | Periodo 4 |
| periodo_5 | NUMERIC(18,2) | Periodo 5 |
| periodo_6 | NUMERIC(18,2) | Periodo 6 |
| total | NUMERIC(18,2) | Total |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pcpotufi`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| codigo_de_la_upr | TEXT | Código de la UPR |
| potencia_de_la_upr_mw | NUMERIC(18,2) | Potencia de la UPR MW |
| codigo_de_la_uf1 | TEXT | Código de la UF1 |
| potencia_uf1_mw | NUMERIC(18,2) | Potencia UF1 MW |
| codigo_de_la_uf2 | TEXT | Código de la UF2 |
| potencia_uf2_mw | NUMERIC(18,2) | Potencia UF2 MW |
| codigo_de_la_uf3 | TEXT | Código de la UF3 |
| potencia_uf3_mw | NUMERIC(18,2) | Potencia UF3 MW |
| codigo_de_la_uf4 | TEXT | Código de la UF4 |
| potencia_uf4_mw | NUMERIC(18,2) | Potencia UF4 MW |
| codigo_de_la_uf5 | TEXT | Código de la UF5 |
| potencia_uf5_mw | NUMERIC(18,2) | Potencia UF5 MW |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pdbaqhmd`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pdsuqhmd`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_penalpmd`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| concepto | TEXT | Concepto |
| en_horas_con_necesidad_del_sistema_a_subir | NUMERIC(18,2) | EN HORAS CON NECESIDAD DEL SISTEMA A SUBIR |
| en_horas_con_necesidad_del_sistema_a_bajar | NUMERIC(18,2) | EN HORAS CON NECESIDAD DEL SISTEMA A BAJAR |
| total_horas | NUMERIC(18,2) | Total horas |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_perddema`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| peaje | TEXT | Peaje |
| dia_1 | NUMERIC(18,1) | Día 1 |
| dia_2 | NUMERIC(18,1) | Día 2 |
| dia_3 | NUMERIC(18,1) | Día 3 |
| dia_4 | NUMERIC(18,1) | Día 4 |
| dia_5 | NUMERIC(18,1) | Día 5 |
| dia_6 | NUMERIC(18,1) | Día 6 |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_perdminqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_perdqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| coeficiente | NUMERIC(18,1) | COEFICIENTE |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_phlqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prdvbaqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prdvdatos`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| frr_subir_mwh | NUMERIC(18,1) | FRR SUBIR MWH |
| frr_bajar_mwh | NUMERIC(18,1) | FRR BAJAR MWH |
| rr_subir_mwh | NUMERIC(18,1) | RR SUBIR MWH |
| rr_bajar_mwh | NUMERIC(18,1) | RR BAJAR MWH |
| desvio_sistema_mwh | NUMERIC(18,3) | DESVIO SISTEMA MWH |
| pbalsub_euros_mwh | NUMERIC(18,2) | PBALSUB EUROS/MWH |
| pbalbaj_euros_mwh | NUMERIC(18,2) | PBALBAJ EUROS/MWH |
| %_frr_minoritaria_s_frr_mayoritaria | NUMERIC(18,3) | % FRR MINORITARIA S/FRR MAYORITARIA |
| precio_unico_dual | TEXT | PRECIO ÚNICO/DUAL |
| precio_dual_de_desvio_a_subir_euros_mwh | NUMERIC(18,2) | PRECIO DUAL DE DESVÍO A SUBIR EUROS/MWH |
| precio_dual_de_desvio_a_bajar_euros_mwh | NUMERIC(18,2) | PRECIO DUAL DE DESVÍO A BAJAR EUROS/MWH |
| precio_unico_de_desvio_euros_mwh | NUMERIC(18,2) | PRECIO UNICO DE DESVÍO EUROS/MWH |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prdvsuqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_premelco`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| tipo | TEXT | Tipo |
| mwh_bc | NUMERIC(18,3) | MWh bc |
| % | NUMERIC(18,1) | % |
| merc_diario | NUMERIC(18,2) | Merc. diario |
| merc_intrad | NUMERIC(18,2) | Merc. intrad |
| rrtt_pbf | NUMERIC(18,2) | RRTT PBF |
| rrtt_p48 | NUMERIC(18,2) | RRTT P48 |
| banda_secundaria_y_rad | NUMERIC(18,2) | Banda secundaria y RAD |
| incump_energ_balance | NUMERIC(18,2) | Incump. energ. balance |
| servicio_rad | NUMERIC(18,2) | Servicio RAD |
| coste_desvios | NUMERIC(18,2) | Coste desvíos |
| saldo_desvios | NUMERIC(18,2) | Saldo desvíos |
| saldo_desvio_sistemas | NUMERIC(18,2) | Saldo desvío sistemas |
| control_fp | NUMERIC(18,2) | Control FP |
| pago_capacidad | NUMERIC(18,2) | Pago capacidad |
| ingreso_control_de_tension | NUMERIC(18,2) | Ingreso Control de tensión |
| total | NUMERIC(18,2) | TOTAL |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prerad`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prinexp`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prinimp`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prqhmi1`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prqhmi2`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prqhmi3`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prrrmedqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prrrqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prrseqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mw | NUMERIC(18,3) | PRECIO (EUR/MW) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prrseqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mw | NUMERIC(18,3) | PRECIO (EUR/MW) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prsecqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prsecqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prterqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_prterqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| precio_eur_mwh | NUMERIC(18,3) | PRECIO (EUR/MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pvpccoms`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | Fecha |
| hora | INTEGER | Hora |
| pmh | NUMERIC(18,2) | Pmh |
| cdsvh | NUMERIC(18,2) | CDSVh |
| precio_energia_excedentaria | NUMERIC(18,2) | Precio energia excedentaria |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pvpcdata`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia | DATE | Día |
| hora | INTEGER | Hora |
| peaje | TEXT | Peaje |
| periodo_p | INTEGER | Periodo p |
| coef_perfil_c__1 | NUMERIC(18,18) | Coef perfil c /1 |
| coef_perdidas_perd__1 | NUMERIC(18,3) | Coef. pérdidas PERD /1 |
| ratio_perd_boe__1 | NUMERIC(18,9) | Ratio PERD/BOE /1 |
| facturacion_energia_feu__mwh_cons | NUMERIC(18,6) | Facturación energía FEU /MWh cons |
| termino_energia_peajes_teup__mwh_cons | NUMERIC(18,3) | Término energía peajes TEUP /MWh cons |
| termino_energia_cargos_teuc__mwh_cons | NUMERIC(18,3) | Término energía cargos TEUC /MWh cons |
| coste_energia_tcu__mwh_cons | NUMERIC(18,6) | Coste energía TCU /MWh cons |
| precio_md+mi1_pm__mwh_bc | NUMERIC(18,2) | Precio MD+MI1 Pm /MWh BC |
| termino_de_ajuste_tae__mwh_bc | NUMERIC(18,5) | Término de ajuste Tae /MWh BC |
| factor_de_correccion_por_energia_fch | NUMERIC(18,5) | Factor de corrección por energía FCh |
| coef_ponderacion_md+mi_a | NUMERIC(18,2) | Coef ponderación MD+MI A |
| coef_ponderacion_mercado_a_plazo_b | NUMERIC(18,2) | Coef ponderación mercado a plazo B |
| precio_medio_aritmetico_pmah__mwh_bc | NUMERIC(18,5) | Precio medio aritmético Pmah /MWh BC |
| precio_medio_cesta_de_futuros_ft__mwh | NUMERIC(18,5) | Precio medio cesta de futuros Ft /MWh |
| precio_medio_futuros_anuales_ano_n_pfanualn | NUMERIC(18,5) | Precio medio futuros anuales año n Pfanualn |
| precio_medio_futuro_trimestral_t_pftrimt | NUMERIC(18,5) | Precio medio futuro trimestral t Pftrimt |
| precio_medio_futuro_mensual_m_pfmensualm | NUMERIC(18,5) | Precio medio futuro mensual m Pfmensualm |
| promedio_de_energia_horaria_del_pdbf_de_cor_dempvpc | NUMERIC(18,1) | Promedio de energía horaria del PDBF de COR DemPVPC |
| aprovisionamiento_esperado_producto_anual_aprovmanualm_mwh | NUMERIC(18,1) | Aprovisionamiento esperado producto anual AprovMAnualm MWh |
| aprovisionamiento_esperado_producto_trimestral_aprovmtrimt_mwh | NUMERIC(18,1) | Aprovisionamiento esperado producto trimestral AprovMTrimt MWh |
| aprovisionamiento_esperado_producto_mensual_aprovmmesm_mwh | NUMERIC(18,1) | Aprovisionamiento esperado producto mensual AprovMMesm MWh |
| servicios_ajuste_sa__mwh_bc | NUMERIC(18,2) | Servicios ajuste SA /MWh BC |
| pago_capacidad_cap__mwh_bc | NUMERIC(18,3) | Pago capacidad CAP /MWh BC |
| financiacion_os_ccos__mwh_bc | NUMERIC(18,5) | Financiación OS CCOS /MWh BC |
| financiacion_om_ccom__mwh_bc | NUMERIC(18,5) | Financiación OM CCOM /MWh BC |
| sinterrum_pibilidad_int__mwh_bc | NUMERIC(18,2) | S.interrum pibilidad INT /MWh BC |
| subastas_renovables_edsr__mwh_bc | NUMERIC(18,3) | Subastas Renovables EDSR /MWh BC |
| rcvtovp__mwh_bc | NUMERIC(18,3) | RCVTOVP /MWH BC |
| ccvh_rfe___mwh_bc | NUMERIC(18,3) | CCVh RFE //MWh bc |
| ccvh_rmrv__mwh_bc | NUMERIC(18,3) | CCVh RMRv /MWh bc |
| ccvh_runitaria__mwh | NUMERIC(18,3) | CCVh RUNITARIA /MWh |
| coste_produccion_cp__mwh_bc | NUMERIC(18,3) | Coste producción CP /MWh BC |
| precio_mdiario_pmd__mwh_bc | NUMERIC(18,2) | Precio m.diario PMD /MWh BC |
| precio_intra_1_pmi1__mwh_bc | NUMERIC(18,2) | Precio intra 1 PMI1 /MWh BC |
| energia_mdiario_emd_mwh_bc | NUMERIC(18,1) | Energía m.diario EMD MWh BC |
| energia_intrad_1_emi1_mwh_bc | NUMERIC(18,2) | Energía intrad 1 EMI1 MWh BC |
| s_ajuste_dia_anterior_pmas1__mwh_bc | NUMERIC(18,2) | S. ajuste día anterior PMAS1 /MWh BC |
| s_ajuste_resto_dia_e_pmas2__mwh_bc | NUMERIC(18,2) | S. ajuste resto día (e) PMAS2 /MWh BC |
| coste_desvio_e_cdsv__mwh_bc | NUMERIC(18,2) | Coste desvío (e) CDSV /MWh BC |
| restricciones_pbf_rt3_d-1_eur | NUMERIC(18,2) | Restricciones PBF RT3 d-1 EUR |
| banda_secundaria_bs3_d-1_eur | NUMERIC(18,2) | Banda secundaria BS3 d-1 EUR |
| reserva_activa_demanda_rad3_d-1_eur | NUMERIC(18,2) | Reserva activa demanda RAD3 d-1 EUR |
| programa_demanda_pbf+mi1_mwh_bc | NUMERIC(18,1) | Programa demanda PBF+MI1 MWh BC |
| restricciones_pbf_rt3_phf1__mwh_bc | NUMERIC(18,2) | Restricciones PBF RT3/PHF1 /MWh BC |
| banda_secundaria_bs3_phf1__mwh_bc | NUMERIC(18,2) | Banda secundaria BS3/PHF1 /MWh BC |
| reserva_activa_demanda_rad3_phf1__mwh_bc | NUMERIC(18,2) | Reserva activa demanda RAD3/PHF1 /MWh BC |
| fecha_calculo | DATE | Fecha cálculo |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_pvpcdatacym`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| dia | DATE | Día |
| hora | INTEGER | Hora |
| peaje | TEXT | Peaje |
| periodo_p | INTEGER | Periodo p |
| coef_perfil_c__1 | NUMERIC(18,18) | Coef perfil c /1 |
| coef_perdidas_perd__1 | NUMERIC(18,3) | Coef. pérdidas PERD /1 |
| ratio_perd_boe__1 | NUMERIC(18,9) | Ratio PERD/BOE /1 |
| facturacion_energia_feu__mwh_cons | NUMERIC(18,6) | Facturación energía FEU /MWh cons |
| termino_energia_peajes_teup__mwh_cons | NUMERIC(18,3) | Término energía peajes TEUP /MWh cons |
| termino_energia_cargos_teuc__mwh_cons | NUMERIC(18,3) | Término energía cargos TEUC /MWh cons |
| coste_energia_tcu__mwh_cons | NUMERIC(18,6) | Coste energía TCU /MWh cons |
| precio_md+mi1_pm__mwh_bc | NUMERIC(18,2) | Precio MD+MI1 Pm /MWh BC |
| termino_de_ajuste_tae__mwh_bc | NUMERIC(18,5) | Término de ajuste Tae /MWh BC |
| factor_de_correccion_por_energia_fch | NUMERIC(18,5) | Factor de corrección por energía FCh |
| coef_ponderacion_md+mi_a | NUMERIC(18,2) | Coef ponderación MD+MI A |
| coef_ponderacion_mercado_a_plazo_b | NUMERIC(18,2) | Coef ponderación mercado a plazo B |
| precio_medio_aritmetico_pmah__mwh_bc | NUMERIC(18,5) | Precio medio aritmético Pmah /MWh BC |
| precio_medio_cesta_de_futuros_ft__mwh | NUMERIC(18,5) | Precio medio cesta de futuros Ft /MWh |
| precio_medio_futuros_anuales_ano_n_pfanualn | NUMERIC(18,5) | Precio medio futuros anuales año n Pfanualn |
| precio_medio_futuro_trimestral_t_pftrimt | NUMERIC(18,5) | Precio medio futuro trimestral t Pftrimt |
| precio_medio_futuro_mensual_m_pfmensualm | NUMERIC(18,5) | Precio medio futuro mensual m Pfmensualm |
| promedio_de_energia_horaria_del_pdbf_de_cor_dempvpc | NUMERIC(18,1) | Promedio de energía horaria del PDBF de COR DemPVPC |
| aprovisionamiento_esperado_producto_anual_aprovmanualm_mwh | NUMERIC(18,1) | Aprovisionamiento esperado producto anual AprovMAnualm MWh |
| aprovisionamiento_esperado_producto_trimestral_aprovmtrimt_mwh | NUMERIC(18,1) | Aprovisionamiento esperado producto trimestral AprovMTrimt MWh |
| aprovisionamiento_esperado_producto_mensual_aprovmmesm_mwh | NUMERIC(18,1) | Aprovisionamiento esperado producto mensual AprovMMesm MWh |
| servicios_ajuste_sa__mwh_bc | NUMERIC(18,2) | Servicios ajuste SA /MWh BC |
| pago_capacidad_cap__mwh_bc | NUMERIC(18,3) | Pago capacidad CAP /MWh BC |
| financiacion_os_ccos__mwh_bc | NUMERIC(18,5) | Financiación OS CCOS /MWh BC |
| financiacion_om_ccom__mwh_bc | NUMERIC(18,5) | Financiación OM CCOM /MWh BC |
| sinterrum_pibilidad_int__mwh_bc | NUMERIC(18,2) | S.interrum pibilidad INT /MWh BC |
| subastas_renovables_edsr__mwh_bc | NUMERIC(18,3) | Subastas Renovables EDSR /MWh BC |
| rcvtovp__mwh_bc | NUMERIC(18,3) | RCVTOVP /MWH BC |
| ccvh_rfe___mwh_bc | NUMERIC(18,3) | CCVh RFE //MWh bc |
| ccvh_rmrv__mwh_bc | NUMERIC(18,3) | CCVh RMRv /MWh bc |
| ccvh_runitaria__mwh | NUMERIC(18,3) | CCVh RUNITARIA /MWh |
| coste_produccion_cp__mwh_bc | NUMERIC(18,3) | Coste producción CP /MWh BC |
| precio_mdiario_pmd__mwh_bc | NUMERIC(18,2) | Precio m.diario PMD /MWh BC |
| precio_intra_1_pmi1__mwh_bc | NUMERIC(18,2) | Precio intra 1 PMI1 /MWh BC |
| energia_mdiario_emd_mwh_bc | NUMERIC(18,1) | Energía m.diario EMD MWh BC |
| energia_intrad_1_emi1_mwh_bc | NUMERIC(18,2) | Energía intrad 1 EMI1 MWh BC |
| s_ajuste_dia_anterior_pmas1__mwh_bc | NUMERIC(18,2) | S. ajuste día anterior PMAS1 /MWh BC |
| s_ajuste_resto_dia_e_pmas2__mwh_bc | NUMERIC(18,2) | S. ajuste resto día (e) PMAS2 /MWh BC |
| coste_desvio_e_cdsv__mwh_bc | NUMERIC(18,2) | Coste desvío (e) CDSV /MWh BC |
| restricciones_pbf_rt3_d-1_eur | NUMERIC(18,2) | Restricciones PBF RT3 d-1 EUR |
| banda_secundaria_bs3_d-1_eur | NUMERIC(18,2) | Banda secundaria BS3 d-1 EUR |
| reserva_activa_demanda_rad3_d-1_eur | NUMERIC(18,2) | Reserva activa demanda RAD3 d-1 EUR |
| programa_demanda_pbf+mi1_mwh_bc | NUMERIC(18,1) | Programa demanda PBF+MI1 MWh BC |
| restricciones_pbf_rt3_phf1__mwh_bc | NUMERIC(18,2) | Restricciones PBF RT3/PHF1 /MWh BC |
| banda_secundaria_bs3_phf1__mwh_bc | NUMERIC(18,2) | Banda secundaria BS3/PHF1 /MWh BC |
| reserva_activa_demanda_rad3_phf1__mwh_bc | NUMERIC(18,2) | Reserva activa demanda RAD3/PHF1 /MWh BC |
| fecha_calculo | DATE | Fecha cálculo |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_resecqhba`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| potencia_mw | NUMERIC(18,3) | POTENCIA (MW) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_resecqhsu`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| potencia_mw | NUMERIC(18,3) | POTENCIA (MW) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_rrsalqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_saldoeneqh`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| fecha_dato | DATE | FECHA |
| hora | INTEGER | HORA |
| qh | INTEGER | QH |
| energia_mwh | NUMERIC(18,3) | ENERGIA (MWh) |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_segmento`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| segmento | TEXT | Segmento |
| descripcion | TEXT | Descripción |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_unifisic`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| instalacion | TEXT | Instalación |
| descripcion_larga | TEXT | Descripción larga |
| tecnologia | TEXT | Tecnología |
| codigo_del_ministerio | TEXT | Código del ministerio |
| fecha_inicio | DATE | Fecha inicio |
| fecha_fin | DATE | Fecha fin |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_uprogram`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| upr | TEXT | UPR |
| tipo_de_oferta | TEXT | Tipo de oferta |
| descripcion | TEXT | Descripción |
| razon_social | TEXT | Razón social |
| eic_upr | TEXT | EIC UPR |
| eic_titular | TEXT | EIC titular |
| tipo_liquidacion | INTEGER | Tipo liquidación |
| titular | TEXT | Titular |
| subsistema | TEXT | Subsistema |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

### Table: `liq_uproufis`
| Column | Type | Source Field |
| :--- | :--- | :--- |
| id | SERIAL | Primary Key |
| upr | TEXT | UPR |
| uf | TEXT | UF |
| desde | DATE | Desde |
| hasta | DATE | Hasta |
| source_file | TEXT | Metadata |
| fecha_proceso | DATE | Metadata |

