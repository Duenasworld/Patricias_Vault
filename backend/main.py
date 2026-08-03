from flask import Flask, request, jsonify  # noqa: I001
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from db_queries import (
    Queries,
    Users,
    PasswordTable,
    TokenKeyTable,
    CreditCardTable,
)


app = Flask(__name__)
CORS(app)  # <-- Neu: Schaltet den Server für Anfragen von Vite frei
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,  # x_for=1: Vertraue einem Proxy bei der Client-IP.
    x_proto=1,  # x_proto=1: Vertraue einem Proxy beim verwendeten Protokoll (http oder https).
)

db = Queries()
user = Users()
ipwd = PasswordTable()
tk = TokenKeyTable()
cc = CreditCardTable()


rc = db.check_db_exists()
print(rc)

if rc == 100:
    db.init_databases()


@app.route("/api/user/erstellen", methods=["POST"])
def daten_speichern():
    # 1. Daten vom Bootstrap-Frontend (JSON) empfangen
    daten: dict | None = request.json

    # Sicherheits-Check: Hat das Frontend überhaupt Daten geschickt?
    if not daten:
        return jsonify({"status": "Fehler", "meldung": "Keine Daten empfangen"}), 400

    # 2. Pflichtfelder aus dem JSON-Paket ziehen
    try:
        username: str = daten["username"]
        first_name: str = daten["first_name"]
        last_name: str = daten["last_name"]
        email: str = daten["email"]
        password_hash: str = daten["password_hash"]
    except KeyError as e:
        # Falls das Frontend ein wichtiges Feld vergessen hat
        return jsonify(
            {"status": "Fehler", "meldung": f"Fehlendes Pflichtfeld: {e}"}
        ), 400

    # 3. Optionale Felder ziehen (Nutzt .get(), um KeyError zu vermeiden, falls sie fehlen)
    middle_name: str | None = daten.get("middle_name")
    comment: str | None = daten.get("comment")

    # 4. Die Logik aus Ihrer Datenbank-Klasse aufrufen
    # (Wir übergeben alle Parameter, inklusive der optionalen)
    neue_user_id: int | None = user.create_test_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
        middle_name=middle_name,
        comment=comment,
    )

    # 5. Antwort an das Frontend zurückgeben
    if neue_user_id:
        return jsonify(
            {
                "status": "Erfolg",
                "meldung": "Benutzer erfolgreich registriert!",
                "user_id": neue_user_id,
            }
        ), 201  # HTTP 201 steht für "Created" (Erfolgreich erstellt)
    else:
        return jsonify(
            {
                "status": "Fehler",
                "meldung": "Benutzername oder E-Mail existiert bereits.",
            }
        ), 409  # HTTP 409 steht für "Conflict" (Datenkonflikt)


# Ganz unten in Ihrer main.py einfügen:

if __name__ == "__main__":
    # Startet den Flask-Server auf Port 5000.
    # debug=True sorgt dafür, dass der Server bei Code-Änderungen automatisch neu startet.
    app.run(port=5000, debug=True)
