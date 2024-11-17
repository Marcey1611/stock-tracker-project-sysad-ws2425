:: !!! In VS-Code vermutlich nicht ausführbar -> Windows-CMD verwenden
@echo off

:: Schritt 1: Docker-Container und Netzwerke herunterfahren und entfernen
echo Stopping and removing containers...
docker-compose down

:: Schritt 2: Docker-Container neu bauen
echo Building containers...
docker-compose build

:: Schritt 3: Docker-Container hochfahren
echo Starting containers...
docker-compose up

:: Warte auf Eingabe, um das Fenster offen zu halten
pause