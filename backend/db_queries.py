import os
import sqlite3
import uuid
from pathlib import Path

db_path = Path("db/pwd.db")


class Queries:
    def __init__(self):
        self.db_path = db_path
        self.db_name = db_path.name
        self.tabellen = []
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

    def setup_sql_statement(self):
        """
        Hier wird das SQL Statement definiert um die vier Tabellen innerhalb der Datenbank zu erstellen. Dieses wird durch die Methode self.setup_tables aufgerufen
        """
        print(f"Start '{self.setup_sql_statement.__name__}'")

        sql_create_statement = [
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_uuid TEXT NOT NULL UNIQUE,  -- Für die eindeutige Identifikation bei der Synchronisation
                username TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                logon_password_hash TEXT NOT NULL,  -- Wichtig: Umbenannt! Hier wird NIEMALS das echte Passwort gespeichert, nur der Hash (z. B. Argon2)
                comment TEXT,
                insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modification_date TEXT DEFAULT CURRENT_TIMESTAMP     
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS internet_pwd_table (
                ip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_uuid TEXT NOT NULL UNIQUE,         -- UUID für den geräteübergreifenden Abgleich
                user_id INTEGER NOT NULL,
                webpage_link TEXT, 
                logon_id TEXT,
                logon_password TEXT,                    -- Hier landet der verschlüsselte Zeichensalat (AES-256)
                logon_pin TEXT,                         -- Hier landet der verschlüsselte Zeichensalat (AES-256)
                active INTEGER DEFAULT 1,               -- Für Soft-Delete (0 = Gelöscht, 1 = Aktiv)
                comment TEXT,
                insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modification_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- Verhindert verwaiste Einträge
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS token_key_table (
                tk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_uuid TEXT NOT NULL UNIQUE,        -- UUID für den geräteübergreifenden Abgleich
                user_id INTEGER NOT NULL,
                internetpage TEXT NOT NULL, 
                token TEXT NOT NULL,                    -- Verschlüsselt
                active INTEGER DEFAULT 1,
                comment TEXT,
                insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modification_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- Verhindert verwaiste Einträge      
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS credit_card_table (
                cc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_uuid TEXT NOT NULL UNIQUE,         -- UUID für den geräteübergreifenden Abgleich
                user_id INTEGER NOT NULL,
                card_type TEXT NOT NULL, 
                card_number TEXT NOT NULL,              -- Verschlüsselt
                validation_code TEXT NOT NULL,          -- Verschlüsselt
                valid_until TEXT NOT NULL,              -- Verschlüsselt
                card_pin TEXT NOT NULL,                 -- Verschlüsselt
                active INTEGER DEFAULT 1,
                comment TEXT,
                insert_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modification_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE -- Verhindert verwaiste Einträge  
            );
            """,
        ]
        print(f"Ende '{self.setup_sql_statement.__name__}'")
        return sql_create_statement

    def init_databases(self):
        """
        Variante A:

        Erstellen der DB und deren Tabellen
        Das SQL Statement selbst wird in der Methode self.sql_create_statement generiert

        Jedes Statement wird einzeln von einem try-except-Block geschützt. Schlägt Tabelle 2 fehl, fängt Python den Fehler ab,
        gibt eine verständliche Fehlermeldung im Terminal aus und macht trotzdem mit Tabelle 3 weiter.
        """
        print(f"Start '{self.init_databases.__name__}'")
        self.delete_db()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.db_name = db_path.name

        # Verbindung zur DB-Datei herstellen (wird erstellt, falls nicht vorhanden)
        with sqlite3.connect(db_path) as conn:
            # WICHTIG: Foreign Keys explizit aktivieren
            conn.execute("PRAGMA foreign_keys = ON;")

            cursor = conn.cursor()
            for statement in self.setup_sql_statement():
                # Wir holen uns den Tabellennamen aus dem String für eine schöne Log-Ausgabe
                table_name = (
                    statement.split("TABLE IF NOT EXISTS")[1].split("(")[0].strip()
                )

                try:
                    cursor.execute(statement)
                    print(f"-> Tabelle '{table_name}' erfolgreich überprüft/erstellt.")
                    self.tabellen.append(table_name)
                except sqlite3.Error as e:
                    print(f"❌ Fehler beim Erstellen der Tabelle '{table_name}': {e}")

            # Änderungen dauerhaft speichern
            conn.commit()
        print(self.tabellen)
        print("🎉 Datenbank-Initialisierung erfolgreich abgeschlossen!\n")
        print(f"Ende '{self.init_databases.__name__}'")

    def setup_tables(self):
        """
        Variante B:
        Erstellen der DB und deren Tabellen
        Das SQL Statement selbst wird in der Methode self.sql_create_statement generiert

        Wenn beim zweiten SQL-Statement ein Fehler auftritt (z. B. ein Tippfehler im SQL oder eine gesperrte Datenbankdatei),
        stürzt Ihr gesamtes Python-Programm sofort ab. Das dritte Statement wird niemals ausgeführt.
        """
        print(f"Start '{self.setup_tables.__name__}'")
        # Verbindung zur Datenbank aufbauen
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                # Die For-Schleife läuft durch alle 3 Statements
                for i, sql in enumerate(self.setup_sql_statement, 1):
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

    def create_test_user(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password_hash: str,
        middle_name: str | None = None,  # Optionaler Parameter mit Standardwert None
        comment: str | None = None,  # Optionaler Parameter mit Standardwert None
    ) -> str | None:  # Rückgabewert ist entweder die UUID (str) oder None
        """
        Fügt einen neuen Benutzer in die Datenbank ein.
        Nutzt Platzhalter (?), um SQL-Injection zu verhindern.
        """
        print(f"Start '{self.create_test_user.__name__}' für Benutzer: {username}")

        # Generiere eine eindeutige UUID für diesen Benutzer (wichtig für die spätere Synchronisation)
        user_uuid = str(uuid.uuid4())

        sql = """
        INSERT INTO users (user_uuid, username, first_name, last_name, email, logon_password_hash, middle_name, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """

        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cursor = conn.cursor()

                # Die Daten werden als Tupel an execute() übergeben -> absolut sicher gegen SQL-Injection
                cursor.execute(
                    sql,
                    (
                        user_uuid,
                        username,
                        first_name,
                        last_name,
                        email,
                        password_hash,
                        middle_name,
                        comment,
                    ),
                )
                conn.commit()

                print(
                    f"✅ Benutzer '{username}' erfolgreich mit UUID {user_uuid} angelegt!"
                )
                return (
                    cursor.lastrowid
                )  # Gibt die generierte user_id (1, 2, 3...) zurück

        except sqlite3.IntegrityError as e:
            # Dieser Fehler tritt auf, wenn z.B. der Username oder die UUID schon existiert (UNIQUE Constraint)
            print(
                f"❌ Fehler: Der Benutzername '{username}' oder die E-Mail ist bereits vergeben. ({e})"
            )
        except sqlite3.Error as e:
            print(f"❌ Allgemeiner Datenbankfehler beim Anlegen des Nutzers: {e}")

        print(f"Ende '{self.create_test_user.__name__}'")
        return None

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


class PasswordTable(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.internet_pwd_table = "internet_pwd_table"


"""
################################################################################################
Token Key Table
################################################################################################
"""


class TokenKeyTable(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.token_key_table = "token_key_table"


"""
################################################################################################
Credit Card Table
################################################################################################
"""


class CreditCardTable(Queries):
    def __init__(self):
        """Initalisieren über Eltern-Klasse"""
        super().__init__()
        self.credit_card_table = "credit_card_table"
