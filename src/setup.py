import sqlite3
from pathlib import Path


# 1. Pfad zur DB (inkl. Subfolder)
db_path = Path("data/db/pwd.db")
db_path.parent.mkdir(parents=True, exist_ok=True)


# 2. SQL Statements
sql_create_statement = [
    """
    CREATE TABLE IF NOT EXISTS internet_pwd_table (
        ip_id INTEGER PRIMARY KEY AUTOINCREMENT,
        webpage_link TEXT NOT NULL, 
        user TEXT,
        password TEXT NOT NULL,
        active INTEGER DEFAULT 1,
        comment TEXT,
        insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
        modification_date TEXT DEFAULT CURRENT_TIMESTAMP       
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS token_key_table (
        tk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        internetpage TEXT NOT NULL, 
        token TEXT NOT NULL,
        active INTEGER DEFAULT 1,
        comment TEXT,
        insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
        modification_date TEXT DEFAULT CURRENT_TIMESTAMP           
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS credit_card_table (
        tk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_type TEXT NOT NULL, 
        card_number TEXT NOT NULL,
        valid_till TEXT NOT NULL,
        card_pin TEXT NOT NULL,
        active INTEGER DEFAULT 1,
        comment TEXT,
        insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
        modification_date TEXT DEFAULT CURRENT_TIMESTAMP       
    );
    """,
]


# 3. Verbindung zur Datenbank aufbauen
try:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Die For-Schleife läuft durch alle 3 Statements
        for i, sql in enumerate(sql_create_statement, 1):
            cursor.execute(sql)
            print(f"✅ Tabelle {i} erfolgreich erstellt!")

        print("\n🎉 Alle Tabellen wurden ohne Fehler angelegt.")

except sqlite3.Error as e:
    # Sobald EIN Statement fehlschlägt, springt Python sofort hierhin
    # Die Schleife wird abgebrochen und weitere Tabellen werden nicht erstellt
    print("\n❌ Fehler abgefangen! Der Prozess wurde gestoppt.")
    print(f"Details zum Fehler: {e}")
