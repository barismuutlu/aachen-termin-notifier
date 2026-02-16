🗓️ Aachen Ausländeramt Termin Notifier

Ein kleines privates Projekt, das automatisch prüft, ob beim Ausländeramt Aachen (RWTH-Studenten) Termine verfügbar sind – und mich per Telegram benachrichtigt, sobald etwas frei wird.

Die Idee ist simpel:
Statt die Seite ständig manuell zu refreshen, übernimmt dieses Script die Arbeit 🙂

✨ Features

✅ Automatische Terminprüfung
✅ Telegram-Benachrichtigung bei freien Terminen 📩
✅ Läuft über GitHub Actions (kein eigener Server nötig)
✅ Sehr leichtgewichtig (kein Browser, nur HTTP-Requests)
✅ Kein Dauer-F5 mehr

⚙️ Wie funktioniert das?

Das Script simuliert den normalen Ablauf auf der Terminseite:

Anliegen auswählen (RWTH Studenten)

Standort bestätigen

Terminseite prüfen

Wenn kein „Kein Termin verfügbar“ gefunden wird → Telegram Nachricht

Alles läuft automatisch über GitHub Actions im Hintergrund.

🚀 Einrichtung
1) Repo klonen

git clone https://github.com/DEIN_USERNAME/aachen-termin-notifier.git

2) Telegram Bot erstellen

Über Telegram @BotFather:

/newbot eingeben
Namen vergeben
Token speichern

3) Chat-ID herausfinden

Dem Bot eine Nachricht schicken und dann im Browser öffnen:

https://api.telegram.org/bot
<TOKEN>/getUpdates

Dort steht:

"chat":{"id":123456789}

Diese Zahl ist deine Chat-ID.

4) GitHub Secrets setzen

Repo → Settings → Secrets → Actions → New secret

Hinzufügen:

TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID

5) Fertig ✅

GitHub Actions prüft automatisch alle 5 Minuten.

Du bekommst nur eine Nachricht, wenn sich der Status ändert (also kein Spam).

💡 Motivation

Die Terminvergabe ist oft ziemlich frustrierend.
Freie Termine sind schnell weg.

Dieses Tool soll einfach helfen, schneller informiert zu sein – mehr nicht.

⚠️ Hinweis / Fair Use

Dieses Projekt ist:

nur für private Nutzung gedacht
nicht für massenhaftes Scraping
nicht für automatisches Buchen
nicht zum Weiterverkauf von Terminen

Bitte fair bleiben 🙏
Die Seite gehört einer Behörde.

🤓 Technisches

Python + requests
Session-Handling über Cookies
GitHub Actions Cronjob
Kein Selenium, kein Browser

📄 Lizenz

Privates Hobbyprojekt.
Nutzung auf eigene Verantwortung.
Keine Garantie, keine Haftung 🙂

☕ Kleine Randnotiz

Falls dir das Tool geholfen hat, freut mich das 😄
War ursprünglich nur für den Eigenbedarf gedacht.

Viel Erfolg beim Termin finden 🍀
