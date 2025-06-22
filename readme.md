# Messagerino
~ Ben Thiemann, Lukas Michalek, Christian Abel, Florian Gründemann
## Database-Tabellen
### Nutzer
- Benutzername TEXT(🔑)
- Anzeigename TEXT
- PasswortHash TEXT
- Erstellungsdatum REAL
### Nachrichten
- UUID TEXT (🔑)
- Sender TEXT
- Empfaenger TEXT
- Inhalt TEXT
- Zeitstempel REAL
- Lesebestaetigung INT