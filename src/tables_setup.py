import os
import sqlite3
from pathlib import Path

# 1. Pfad zur DB (inkl. Subfolder)
db_path = Path("db/pwd.db")


def setup_tables():
    db_path.parent.mkdir(parents=True, exist_ok=True)
    # 2. SQL Statements
    sql_create_statement = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            logon_password TEXT NOT NULL,
            comment TEXT,
            insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
            modification_date TEXT DEFAULT CURRENT_TIMESTAMP     
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS internet_pwd_table (
            ip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            webpage_link TEXT NOT NULL, 
            logon_id TEXT,
            logon_password TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            comment TEXT,
            insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
            modification_date TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS token_key_table (
            tk_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
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
            cc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            card_type TEXT NOT NULL, 
            card_number TEXT NOT NULL,
            validation_code INTEGER NOT NULL,
            valid_until TEXT NOT NULL,
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


def delete_db():

    if os.path.exists(db_path):
        db_path.unlink()  # Löscht die Datei
        print(f"Datenbank '{db_path.name}' gelöscht.")
    else:
        print(f"Datenbank '{db_path.name}' existiert nicht")
