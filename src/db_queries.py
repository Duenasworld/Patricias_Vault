import os
import sqlite3
from pathlib import Path

db_path = Path("db/pwd.db")


class Queries:
    def __init__(self):
        self.db_path = db_path
        self.db_name = db_path.name
        self.tabellen = []
        self.sql_statement = None
        self.sql_code = 999
        self.sql_errortext = None

    def check_db_exists(self):
        """
        Check if the database exists already or if it needs to be created first
        """
        print(f"Start '{self.check_db_exists.__name__}'")
        self.sql_code = 0

        # 1. Prüfen, ob die Datei existiert

        if os.path.exists(self.db_path):
            print(f"Die Datenbank '{self.db_name}' existiert bereits.")

            # Verbindung herstellen
            # connection = sqlite3.connect(self.db_name)
            # print(connection.total_changes)

        else:
            self.sql_code = 100
            print(
                f"Die Datenbank '{self.db_name}' existiert noch nicht, bitte setup programm ausführen"
            )

        print(f"Ende '{self.check_db_exists.__name__}'")
        return self.sql_code

    def setup_tables(self):
        print(f"Start '{self.setup_tables.__name__}'")
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

                print("\n🎉 Folgende Tabellen wurden ohne Fehler angelegt:")

                cursor.execute("""
                    SELECT name 
                    FROM sqlite_master 
                    WHERE type='table';
                """)

                # Ergebnis auswerten
                self.tabellen = cursor.fetchall()

                for tabelle in self.tabellen:
                    print(tabelle[0])

                self.sql_code = 0

        except sqlite3.Error as e:
            # Sobald EIN Statement fehlschlägt, springt Python sofort hierhin
            # Die Schleife wird abgebrochen und weitere Tabellen werden nicht erstellt
            print("\n❌ Fehler abgefangen! Der Prozess wurde gestoppt.")
            print(f"Details zum Fehler: {e}")
            self.sql_code = 999

        print(f"Ende '{self.setup_tables.__name__}'")
        return self.sql_code

    def delete_db(self):
        print(f"Start '{self.delete_db.__name__}'")
        if self.db_path.exists():
            self.db_path.unlink()  # Löscht die Datei
            print(f"Datenbank '{self.db_name}' gelöscht.")
            self.db_name = None
            self.db_path = None
        print(f"Ende '{self.delete_db.__name__}'")


"""
################################################################################################
User Table
################################################################################################
"""


class Users(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.user_table = "users"
        self.username = None
        self.user_id = 0

    def select_users(self):
        connection = sqlite3.connect(self.db_path)
        print(connection.total_changes)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM example")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        connection.close()

    def insert_user(self):
        connection = sqlite3.connect(self.db_path)
        print(connection.total_changes)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users VALUES (1, 'alice', 20)")
        cursor.execute("INSERT INTO example VALUES (2, 'bob', 30)")
        cursor.execute("INSERT INTO example VALUES (3, 'eve', 40)")

        connection.commit()
        connection.close()

    def delete_user(self, username: str, user_id: int):
        self.username = username
        self.user_id = user_id
        return self.sql_code


"""
################################################################################################
Internet PWD table
################################################################################################
"""


class Internet_PWD_DB(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.internet_pwd_table = "internet_pwd_table"


"""
################################################################################################
Token Key Table
################################################################################################
"""


class Token_Key_Table(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.token_key_table = "token_key_table"


"""
################################################################################################
Credit Card Table
################################################################################################
"""


class Credit_Card_Table(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.credit_card_table = "credit_card_table"
