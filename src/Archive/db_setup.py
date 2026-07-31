import os
import sqlite3
from pathlib import Path


class Queries:
    def __init__(self, db_name: str = None):
        self.db_name = db_name
        self.db_path = None
        self.sql_statement = None
        self.sql_code = 999
        self.sql_errortext = None

    def check_db_exists(self, db_name: str = None, create: bool = False):
        self.sql_code = 0
        self.db_name = db_name

        # 1. Prüfen, ob die Datei existiert
        if os.path.exists(self.db_name):
            print(f"Die Datenbank '{self.db_name}' existiert bereits.")

            # Verbindung herstellen
            conn = sqlite3.connect(self.db_name)
        else:
            self.sql_code = 100
            print(
                f"Die Datenbank '{self.db_name}' existiert noch nicht und wird jetzt angelegt: {create}"
            )

            if create:
                # Verbindung herstellen
                conn = sqlite3.connect(self.db_name)
                print(f"Die Datenbank '{self.db_name}' wurde angelegt.")
                self.sql_code = 0

        return self.sql_code

    def delete_db(self, db_name: str = None):
        db_pfad = Path(db_name)

        if db_pfad.exists():
            db_pfad.unlink()  # Löscht die Datei
            print(f"Datenbank '{self.db_name}' gelöscht.")
            self.db_name = None

    def check_table_exists(self, table_name: str = None):
        print(
            f"Prüfen ob die Datenbank '{self.db_name}' und die Tabelle '{table_name}' existieren."
        )
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )

        # Ergebnis auswerten
        if cursor.fetchone():
            self.sql_code = 0
            self.sql_errortext = f"Die Tabelle '{table_name}' existiert bereits."
        else:
            self.sql_code = 100
            self.sql_errortext = f"Die Tabelle '{table_name}' existiert noch nicht."

        print(self.sql_errortext, self.sql_code)

        conn.close()
        return self.sql_code


class Internet_PWD_DB(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.internet_pwd_table = "internet_pwd_table"

    def check_ipwd_table_exists(self, db_name: str = None):
        self.db_name = db_name
        print(
            f"Prüfen mittels check_ipwd_table_exists ob in der Datenbank '{self.db_name}' die Tabelle '{self.internet_pwd_table}' existiert."
        )
        return super().check_table_exists(self.internet_pwd_table)

    def create_internet_pwd_table(self):
        print("self.db_name", self.db_name)
        sql_create_table = """
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
        """

        try:
            # 2. Verbindung öffnen (wird durch 'with' automatisch wieder geschlossen)
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # 3. Statement ausführen
                cursor.execute(sql_create_table)

                # Wenn der Code hier ankommt, gab es keinen Fehler
                print(
                    "✅ Tabelle wurde erfolgreich erstellt (oder existierte bereits)!"
                )
                self.sql_code = 0
        except sqlite3.Error as e:
            # Falls z.B. ein Syntaxfehler im SQL-Text ist, wird das hier abgefangen
            print(f"❌ Fehler beim Erstellen der Tabelle: {e}")
            self.sql_code = 999

        return self.sql_code


class Token_Key_Table(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.token_key_table = "token_key_table"

    def check_tk_table_exists(self, db_name: str = None):
        self.db_name = db_name
        return super().check_table_exists(self.token_key_table)

    def create_internet_pwd_table(self):
        print("self.db_name", self.db_name)
        sql_create_table = """


        try:
            # 2. Verbindung öffnen (wird durch 'with' automatisch wieder geschlossen)
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # 3. Statement ausführen
                cursor.execute(sql_create_table)

                # Wenn der Code hier ankommt, gab es keinen Fehler
                print(
                    "✅ Tabelle wurde erfolgreich erstellt (oder existierte bereits)!"
                )
                self.sql_code = 0
        except sqlite3.Error as e:
            # Falls z.B. ein Syntaxfehler im SQL-Text ist, wird das hier abgefangen
            print(f"❌ Fehler beim Erstellen der Tabelle: {e}")
            self.sql_code = 999

        return self.sql_code


class Credit_Card_Table(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.credit_card_table = "credit_card_table"

    def check_cd_table_exists(self, db_name: str = None):
        self.db_name = db_name
        return super().check_table_exists(self.token_key_table)

    def create_cd_table(self):
        print("self.db_name", self.db_name)
        sql_create_table = """
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
        """

        try:
            # 2. Verbindung öffnen (wird durch 'with' automatisch wieder geschlossen)
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # 3. Statement ausführen
                cursor.execute(sql_create_table)

                # Wenn der Code hier ankommt, gab es keinen Fehler
                print(
                    "✅ Tabelle wurde erfolgreich erstellt (oder existierte bereits)!"
                )
                self.sql_code = 0
        except sqlite3.Error as e:
            # Falls z.B. ein Syntaxfehler im SQL-Text ist, wird das hier abgefangen
            print(f"❌ Fehler beim Erstellen der Tabelle: {e}")
            self.sql_code = 999

        return self.sql_code
