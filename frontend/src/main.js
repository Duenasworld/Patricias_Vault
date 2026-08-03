// 1. Bootstrap CSS & JS importieren (Vite holt das automatisch aus node_modules)
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// 2. DOM-Elemente greifen
const registerForm = document.getElementById('registerForm');
const statusMessage = document.getElementById('statusMessage');

// 3. Event-Listener für das Absenden des Formulars
registerForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Verhindert das Neuladen der Seite

    // Daten aus den Eingabefeldern sammeln
    const payload = {
        username: document.getElementById('username').value,
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        // Aktuell schicken wir das Passwort temporär direkt mit (GUI-Test)
        password_hash: document.getElementById('password').value, 
        middle_name: document.getElementById('middleName').value || null, // str | None
        comment: document.getElementById('comment').value || null        // str | None
    };

    console.log("Das schickt das Frontend los:", payload);

    try {
        // API-Anfrage an Ihren Flask-Server senden
        const response = await fetch('http://localhost:5000/api/user/erstellen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // Statusmeldung im GUI anzeigen
        statusMessage.classList.remove('d-none', 'alert-danger', 'alert-success');
        
        if (response.ok) {
            statusMessage.classList.add('alert-success');
            statusMessage.innerText = `🎉 ${result.meldung} (User-ID: ${result.user_id})`;
            registerForm.reset(); // Formular leeren
        } else {
            statusMessage.classList.add('alert-danger');
            statusMessage.innerText = `❌ ${result.meldung}`;
        }

    } catch (error) {
        statusMessage.classList.remove('d-none');
        statusMessage.classList.add('alert-danger');
        statusMessage.innerText = '❌ Verbindung zum Python-Server fehlgeschlagen.';
    }
});
