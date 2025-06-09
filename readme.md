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
- Empfänger TEXT
- Inhalt TEXT
- Zeitstempel REAL
- Lesebestätigung INT