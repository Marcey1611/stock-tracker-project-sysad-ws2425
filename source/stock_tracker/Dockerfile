# Verwende ein existierendes Flutter-Image mit einer aktuellen Dart SDK
FROM mobiledevops/flutter-sdk-image:latest as build

# Erstelle den flutteruser und die Gruppe
RUN groupadd flutteruser && useradd -g flutteruser flutteruser

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere den aktuellen Projektinhalt in das Containerverzeichnis
COPY . .

# Git als sicher für Flutter konfigurieren (als Root ausführen)
RUN git config --global --add safe.directory /home/mobiledevops/.flutter-sdk

# Bereinige den Flutter- und Dart-Cache
RUN flutter clean && dart pub cache clean

# Setze die Berechtigungen für alle Dateien, damit flutteruser darauf zugreifen kann
RUN chown -R flutteruser:flutteruser /app /home/mobiledevops/.flutter-sdk /home/mobiledevops/.pub-cache

# Wechsle zu flutteruser
USER flutteruser

# Sicherstellen, dass alle Abhängigkeiten heruntergeladen werden
RUN flutter pub get

# Installiere Abhängigkeiten und baue das Flutter-Webprojekt
RUN flutter build web

# Produktions-Phase mit Nginx
FROM nginx:stable-alpine

# Kopiere das gebaute Ergebnis in das Nginx-Verzeichnis
COPY --from=build /app/build/web /usr/share/nginx/html

# Exponiere Port 80
EXPOSE 80

# Starte den Nginx-Webserver
CMD ["nginx", "-g", "daemon off;"]
