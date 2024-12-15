# Verwenden eines Flutter-Images
FROM cirrusci/flutter:latest

# Erstelle einen Nicht-Root-Benutzer
RUN useradd -ms /bin/bash flutteruser

# Wechsle in das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die App-Dateien
COPY . /app

# Installiere notwendige Abhängigkeiten
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    libglu1-mesa \
    openjdk-11-jdk

# Git als sicher für Flutter konfigurieren (als Root ausführen)
RUN git config --global --add safe.directory /sdks/flutter

# Berechtigungen setzen, damit der flutteruser auf das Verzeichnis zugreifen kann
RUN chown -R flutteruser:flutteruser /sdks/flutter

# Wechsle zu flutteruser
USER flutteruser
#neuestes Version
#RUN flutter upgrade

# Sicherstellen, dass alle Abhängigkeiten heruntergeladen werden
RUN flutter pub get

# Baue die Flutter-Webanwendung
RUN flutter build web

# Setze den Webserver (nginx)
FROM nginx:alpine

# Kopiere die gebauten Webdateien in den Nginx-Server
COPY --from=0 /app/build/web /usr/share/nginx/html

# Exponiere den Port
EXPOSE 80