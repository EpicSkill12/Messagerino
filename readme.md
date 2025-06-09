# Messagerino
~ Ben Thiemann & Lukas Michalek
## Datenbank-Tabellen
### Nutzer
- Nutzername TEXT(🔑)
- Anzeigename TEXT
- PasswortHash TEXT
- Erstellungsdatum REAL
### Nachrichten
- UUID TEXT (🔑)
- Absender TEXT
- Empfaenger TEXT
- Inhalt TEXT
- Zeitstempel REAL
- Lesebestaetigung INT