
import sqlite3
def extract_schema(db_path, sample_rows=2, verbose=True):
    """
    Extrahiert das Schema aller Tabellen in der SQLite-Datenbank und gibt
    – abhängig vom Parameter verbose – entweder die Ergebnisse aus oder liefert sie als Dictionary zurück.
    
    Parameter:
      - db_path: Pfad zur Datenbank.
      - sample_rows: Anzahl der Beispielzeilen, die pro Tabelle abgerufen werden.
      - verbose: Falls True, werden die Informationen direkt ausgegeben.
      
    Rückgabe:
      Ein Dictionary, in dem für jede Tabelle die folgenden Informationen enthalten sind:
        - columns: Liste der Spalten (inkl. Typ und Kennzeichnung als PK)
        - foreign_keys: Liste der Fremdschlüssel (Format: "Spalte -> referenzierteTabelle.referenzierteSpalte")
        - sample_data: Abgerufene Beispieldaten (als Liste von Zeilen)
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Alle Tabellennamen abrufen
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]
    
    schema = {}
    
    for table in table_names:
        if verbose:
            print(f"Schema for Table '{table}':")
        
        # Spalteninformationen abrufen
        cursor.execute(f"PRAGMA table_info({table});")
        columns_info = cursor.fetchall()  
        columns = []
        for col in columns_info:
            col_name = col[1]
            col_type = col[2]
            is_pk = " (PK)" if col[5] != 0 else ""
            columns.append(f"{col_name} {col_type}{is_pk}")
        if verbose:
            print("Columns:", ", ".join(columns))
        
        # Fremdschlüsselinformationen abrufen
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fk_info = cursor.fetchall()  
        foreign_keys = []
        for fk in fk_info:
            foreign_keys.append(f"{fk[3]} -> {fk[2]}.{fk[4]}")
        if verbose:
            if foreign_keys:
                print("Foreign Keys:", ", ".join(foreign_keys))
            else:
                print("Foreign Keys: none")
        
        # Beispiel-Daten abrufen
        cursor.execute(f"SELECT * FROM {table} LIMIT {sample_rows};")
        sample_data = cursor.fetchall()
        if verbose:
            print("Sample data:", sample_data)
            print("-" * 80)
        
        schema[table] = {
            "columns": columns,
            "foreign_keys": foreign_keys,
            "sample_data": sample_data
        }
    
    conn.close()
    return schema

import re
def extract_sql_statement(text: str) -> str:
    """
    Extracts the SQL statement from a given text, starting from "SELECT" 
    until the first semicolon ";".
    """
    pattern = r'(SELECT.*?;)'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

