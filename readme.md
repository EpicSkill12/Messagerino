# Messagerino
~ Ben Thiemann, Lukas Michalek, Christian Abel, Florian Gründemann
## Database-Tabellen
### User
- Username TEXT(🔑)
- DisplayName TEXT
- PasswortHash TEXT
- Erstellungsdatum REAL
### Messageen
- UUID TEXT (🔑)
- Sender TEXT
- Empfänger TEXT
- Content TEXT
- Zeitstempel REAL
- Lesebestätigung INT