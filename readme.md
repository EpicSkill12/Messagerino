# Messagerino
~ Ben Thiemann & Lukas Michalek
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
- SendTime REAL
- Lesebestätigung INT