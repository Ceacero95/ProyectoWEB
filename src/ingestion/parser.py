import io
import zipfile
import pandas as pd
import logging
import re

logger = logging.getLogger(__name__)

class DataParser:
    """
    Parses raw bytes (Zips/Excels) into meaningful DataFrames.
    Includes logic to normalizing I90 files (Horizontal/Vertical).
    """

    @staticmethod
    def extract_zip(zip_bytes: bytes) -> dict[str, bytes]:
        extracted = {}
        try:
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                for name in z.namelist():
                    extracted[name] = z.read(name)
        except zipfile.BadZipFile:
            logger.error("Invalid ZIP file.")
        return extracted

    @staticmethod
    def parse_i90_excel(file_bytes: bytes, filename_ref: str = "") -> dict[str, dict]:
        """
        Parses I90 PDBF Excel with specific sheet configuration.
        Returns a dict of {table_name: {'df': DataFrame, 'pk': [list_of_cols]}}
        """
        SHEET_CONFIG = {
            "I90DIA01": 3, "I90DIA02": 3, "I90DIA03": 2, "I90DIA04": 2,
            "I90DIA05": 2, "I90DIA06": 2, "I90DIA07": 2, "I90DIA08": 2,
            "I90DIA09": 2, "I90DIA10": 2, "I90DIA11": 2, "I90DIA12": 2,
            "I90DIA13": 2, "I90DIA14": 2, "I90DIA15": 2, "I90DIA16": 0,
            "I90DIA17": 2, "I90DIA18": 1, "I90DIA19": 3, "I90DIA20": 3,
            "I90DIA21": 3, "I90DIA22": 2, "I90DIA23": 2, "I90DIA24": 2,
            "I90DIA25": 2, "I90DIA26": 3, "I90DIA27": 3, "I90DIA28": 2,
            "I90DIA29": 1, "I90DIA30": 2, "I90DIA31": 2, "I90DIA32": 2,
            "I90DIA33": 1, "I90DIA34": 2, "I90DIA35": 2, "I90DIA36": 3,
            "I90DIA37": 2, "I90DIA38": 2, "I90DIA39": 3, "I90DIA40": 3,
            "I90DIA41": 2, "I90DIA42": 2
        }
        results = {}
        try:
            xl = pd.ExcelFile(io.BytesIO(file_bytes))
            sheet_names = xl.sheet_names

            ref_date_val, pub_date_val = None, None
            if "I90DIA00" in sheet_names:
                try:
                    df00 = xl.parse("I90DIA00", header=None, nrows=10)
                    ref_date_val = df00.iloc[5, 0]
                    pub_date_val = df00.iloc[5, 2]
                except Exception as e:
                    logger.warning(f"Could not extract dates from I90DIA00: {e}")
            
            for sheet in sheet_names:
                if sheet not in SHEET_CONFIG:
                    continue
                
                try:
                    header_row = SHEET_CONFIG[sheet]
                    
                    # First check if sheet has enough rows
                    df_check = xl.parse(sheet, header=None, nrows=header_row + 2)
                    if len(df_check) <= header_row:
                        logger.warning(f"Sheet {sheet} has insufficient rows (only {len(df_check)} rows, needs > {header_row}). Skipping.")
                        continue
                    
                    df = xl.parse(sheet, header=header_row)
                    if df.empty:
                        logger.warning(f"Sheet {sheet} is empty after parsing. Skipping.")
                        continue
                    
                    table_name = sheet.lower() + "_hist"
                    df.columns = [str(c).strip() for c in df.columns]

                    # --- COLUMN RENAMING ---
                    rename_map = {}
                    for col in df.columns:
                        col_low = col.lower()
                        if "unidad de programación" in col_low:
                            rename_map[col] = "up"
                        elif "unidad física" in col_low or "unidad fisica" in col_low:
                            rename_map[col] = "uf"
                        elif "bloque" in col_low:
                            rename_map[col] = "bloque"
                        elif "sentido" in col_low:
                            rename_map[col] = "sentido"
                    df.rename(columns=rename_map, inplace=True)

                    # Drop 'Total' columns if they exist
                    total_cols = [c for c in df.columns if 'total' in str(c).lower()]
                    if total_cols:
                        df.drop(columns=total_cols, inplace=True)

                    normalized_df, dimensions = DataParser._normalize_i90_sheet(df, table_name)
                        
                    if normalized_df is not None and not normalized_df.empty:
                        ref_ts = pd.to_datetime(ref_date_val, errors='coerce')
                        pub_ts = pd.to_datetime(pub_date_val, errors='coerce')
                        normalized_df['fecha'] = ref_ts.date() if pd.notnull(ref_ts) else None
                        if 'fecha_publicacion' not in normalized_df.columns:
                            normalized_df['fecha_publicacion'] = pub_ts.date() if pd.notnull(pub_ts) else None

                        resolucion = 'H' 
                        if 'periodo' in normalized_df.columns:
                            try:
                                max_p = normalized_df['periodo'].max()
                                if int(max_p) > 25: resolucion = 'QH'
                            except: pass
                        normalized_df['resolucion'] = resolucion
                        
                        # PK: Dimensions before periods + source_file
                        # We also include 'periodo' and 'fecha' as they are part of the record's identity in long format
                        pk = dimensions + ['source_file']
                        if 'periodo' in normalized_df.columns and 'periodo' not in pk:
                            pk.append('periodo')
                        if 'fecha' in normalized_df.columns and 'fecha' not in pk:
                            pk.append('fecha')
                        
                        # Filter PK columns that actually exist in normalized_df
                        pk = [c for c in pk if c in normalized_df.columns]
                        
                        results[table_name] = {
                            'df': normalized_df,
                            'pk': pk
                        }
                        logger.info(f"Successfully processed sheet {sheet} -> {table_name} ({len(normalized_df)} rows)")
                    else:
                        logger.warning(f"Sheet {sheet} produced empty normalized data. Skipping.")
                
                except Exception as e:
                    logger.error(f"Error processing sheet {sheet}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    continue
                
        except Exception as e:
            logger.error(f"Error parsing I90 Excel ({filename_ref}): {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Don't raise - return what we have so far
            
        logger.info(f"Completed parsing {filename_ref}: {len(results)} tables extracted")
        return results
    
    @staticmethod
    def _normalize_i90_sheet(df: pd.DataFrame, table_name: str) -> tuple[pd.DataFrame, list[str]]:
        """
        Detects if Horizontal or Vertical and returns a long-format DataFrame and dimension columns.
        """
        cols = list(df.columns)
        
        # 1. Detect Horizontal (H1, E1... or 1 MW, 1 (€/MW)... or mw1, €/mw1... or 01-02... style)
        col_strs = [str(c).strip() for c in cols]
        has_h1 = any(c.lower() == 'h1' for c in col_strs)
        has_e1 = any(c.lower() == 'e1' for c in col_strs)
        
        # New patterns: 1 MW, 1 (€/MW), mw1, mwh1, €/mw1, €/mwh1, 01-02, 1, 2, 3
        # Use more robust counting for purely numeric or hyphenated periods
        def is_numeric(s):
            return s.replace('.0','').isdigit() or s.isdigit() or re.match(r'^\d+', s)
            
        num_numeric = sum(1 for c in col_strs if is_numeric(c) and not c.startswith('Unnamed'))
        has_numeric_headers = num_numeric > 5
        
        has_compact_headers = any(re.search(r'(mw|mwh|€/mw|€/mwh|ç/mw|ç/mwh)\d+', c, re.I) for c in col_strs)
        has_hyphen_headers = any(re.search(r'^\d+-\d+', c) for c in col_strs)
        has_unit_keyword = any(re.search(r'(mw|mwh|ç/mw|ç/mwh|€/mw|€/mwh|precio|potencia|energia|cuarto de hora)', c, re.I) for c in col_strs)
        
        # New: check for duplicated headers that often imply horizontal periodicity (Precio, Precio.1, etc)
        def has_duplicated_headers(lst):
            base_names = [re.sub(r'\.\d+$', '', n) for n in lst if not n.startswith('Unnamed')]
            counts = pd.Series(base_names).value_counts()
            return any(counts > 5)

        if (has_h1 and has_e1) or has_numeric_headers or has_compact_headers or has_hyphen_headers or has_unit_keyword or has_duplicated_headers(col_strs):
             return DataParser._melt_horizontal_i90(df)
        
        # 2. Detect Vertical (Periodo/Hora column)
        is_vertical = any(c.lower() in ['hora', 'periodo'] for c in col_strs)
        
        if is_vertical:
            return DataParser._standardize_vertical_i90(df)
            
        # Fallback: Return as is
        logger.warning(f"Could not detect structure for {table_name}. Returning raw.")
        # Minimal cleanup
        df.columns = [str(c).lower().replace(" ", "_").replace(".", "") for c in df.columns]
        # Dimensions are all columns for now
        return df, list(df.columns)

    @staticmethod
    def _melt_horizontal_i90(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms wide format (H1..H24, E1..E24) to long format (Periodo, Energia, Precio).
        """
        # Identify ID columns and Period/Value columns
        id_vars = []
        value_vars = [] # List of tuples (original_col, periodo, value_type)
        
        for c in df.columns:
            c_str = str(c).strip()
            c_low = c_str.lower()
            periodo = None
            v_type = None
            
            # 1. Case: H1/E1 (Prefix + Period)
            mh = re.match(r'^([He])(\d+)$', c_low)
            if mh:
                v_type = 'precio' if mh.group(1) == 'h' else 'energia'
                periodo = int(mh.group(2))
            
            # 2. Case: Hyphen (01-02)
            if periodo is None:
                mhy = re.match(r'^(\d+)-(\d+)', c_str)
                if mhy:
                    periodo = int(mhy.group(2))
                    if any(x in c_low for x in ['ç', '€', 'precio']): v_type = 'precio'
                    elif 'mwh' in c_low or 'energia' in c_low: v_type = 'energia'
                    elif 'mw' in c_low or 'potencia' in c_low: v_type = 'potencia'
                    else: v_type = 'valor'
            
            # 3. Case: Suffix/Prefix units + period (mw1, mwh1, €/mw1...)
            if periodo is None:
                # Use search for flexibility if embedded
                mcp = re.search(r'(mw|mwh|€/mw|€/mwh|ç/mw|ç/mwh|precio|potencia|energia|valor)(\d+)$', c_low)
                if mcp:
                    pre = mcp.group(1)
                    periodo = int(mcp.group(2))
                    if any(x in pre for x in ['ç', '€', 'precio']): v_type = 'precio'
                    elif 'mwh' in pre or 'energia' in pre: v_type = 'potencia' if 'mw' in pre else 'energia' # Following plan: mw/mwh -> potencia for these specific sheets
                    elif 'mw' in pre or 'potencia' in pre: v_type = 'potencia'
                    else: v_type = 'valor'
                    
                    # Plan refinement: mw(\d+) and mwh(\d+) -> potencia
                    if pre in ['mw', 'mwh']: v_type = 'potencia'

            # 4. Case: Numeric prefix (1 MW) or pure number (1)
            if periodo is None:
                mnp = re.match(r'^(\d+)', c_str)
                if mnp:
                    periodo = int(mnp.group(1))
                    if any(x in c_low for x in ['ç', '€', 'precio']): v_type = 'precio'
                    elif 'mwh' in c_low or 'energia' in c_low: v_type = 'potencia' if 'mw' in c_low else 'energia'
                    elif 'mw' in c_low or 'potencia' in c_low: v_type = 'potencia'
                    else: v_type = 'valor'
                    
                    # Plan refinement: mw and mwh patterns -> potencia
                    if re.search(r'(mw|mwh)', c_low): v_type = 'potencia'
            
            # 5. Case: Flexible unit matching at the end of long column names
            if periodo is None:
                mflex = re.search(r'(mw|mwh|€/mw|€/mwh|ç/mw|ç/mwh)(?:\.(\d+))?$', c_low)
                if mflex:
                    pre = mflex.group(1)
                    suf_p = mflex.group(2)
                    periodo = int(suf_p) + 1 if suf_p else 1
                    if any(x in pre for x in ['ç', '€', 'precio']): v_type = 'precio'
                    else: v_type = 'potencia' # mw/mwh -> potencia per plan

            # 6. Case: Pandas Duplicates (Name.1) or Generic Keyword
            if periodo is None:
                found_type = None
                if any(x in c_low for x in ['ç', '€', 'precio']): 
                    found_type = 'precio'
                elif 'mwh' in c_low or 'energia' in c_low: 
                    found_type = 'potencia' if 'mw' in c_low else 'energia'
                elif 'mw' in c_low or 'potencia' in c_low: 
                    found_type = 'potencia'
                elif 'valor' in c_low:
                    found_type = 'valor'
                
                if found_type:
                    v_type = found_type
                    # Check for suffix .n
                    msuf = re.search(r'\.(\d+)$', c_str)
                    if msuf:
                        periodo = int(msuf.group(1)) + 1
                    else:
                        periodo = 1
            
            if periodo is not None:
                value_vars.append((c, periodo, v_type if v_type else 'valor'))
            else:
                id_vars.append(c)

        if not value_vars:
            return df
            
        # Add a row index to prevent merge issues
        df['row_id_melt'] = range(len(df))
        id_vars_with_row = id_vars + ['row_id_melt']
        
        # Melt per type
        melted_parts = []
        unique_types = sorted(list(set(v[2] for v in value_vars)))
        
        for vt in unique_types:
            # Columns of this type
            type_cols = [col for col, p, vtag in value_vars if vtag == vt]
            col_to_period = {col: p for col, p, vtag in value_vars if vtag == vt}
            
            t_melt = df.melt(id_vars=id_vars_with_row, value_vars=type_cols, var_name='periodo_raw', value_name=vt)
            t_melt['periodo'] = t_melt['periodo_raw'].map(col_to_period)
            t_melt.drop(columns=['periodo_raw'], inplace=True)
            melted_parts.append(t_melt)
            
        # Merge all types
        result = melted_parts[0]
        for part in melted_parts[1:]:
            result = pd.merge(result, part, on=id_vars_with_row + ['periodo'], how='outer')
            
        result.drop(columns=['row_id_melt'], inplace=True)
        # Final cleanup: lowercase and remove special chars
        result.columns = [str(c).lower().replace(" ", "_").replace(".", "").replace("(", "").replace(")", "").replace("/", "_") for c in result.columns]
        result.drop_duplicates(inplace=True)
        
        # Dimension columns (id_vars) cleaned for final output
        clean_dimensions = [str(c).lower().replace(" ", "_").replace(".", "").replace("(", "").replace(")", "").replace("/", "_") for c in id_vars if str(c) != 'row_id_melt']
        
        # CRITICAL: Remove 'hora' if it exists in dimensions or columns
        if 'hora' in result.columns:
            result.drop(columns=['hora'], inplace=True)
        clean_dimensions = [d for d in clean_dimensions if d != 'hora']

        return result, clean_dimensions

    @staticmethod
    def _standardize_vertical_i90(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
        """
        Standardizes vertical files and identifies dimension columns.
        """
        # Rename 'Hora' -> 'periodo'
        df = df.rename(columns=lambda x: str(x).strip())
        rename_map = {}
        dimensions = []
        for c in df.columns:
            c_str = str(c).lower()
            if c_str == 'hora' or c_str == 'periodo':
                rename_map[c] = 'periodo'
            else:
                dimensions.append(c)
        
        df.rename(columns=rename_map, inplace=True)
        
        # Final cleanup: lowercase and remove special chars
        df.columns = [str(c).lower().replace(" ", "_").replace(".", "").replace("(", "").replace(")", "").replace("/", "_") for c in df.columns]
        
        # Clean dimensions as well
        clean_dimensions = [str(c).lower().replace(" ", "_").replace(".", "").replace("(", "").replace(")", "").replace("/", "_") for c in dimensions]
        
        # CRITICAL: Remove 'hora' if it exists in dimensions or columns
        if 'hora' in df.columns:
            df.drop(columns=['hora'], inplace=True)
        clean_dimensions = [d for d in clean_dimensions if d != 'hora']

        return df, clean_dimensions

    @staticmethod
    def parse_liquicomun_zip(zip_bytes: bytes) -> tuple[str, dict[str, bytes]]:
        files = DataParser.extract_zip(zip_bytes)
        subtype = "unknown"
        for name in files.keys():
            if "_" in name:
                possible = name.split("_")[0]
                if len(possible) <= 3:
                    subtype = possible
                    break
        return subtype, files
