FROM mobiledevops/flutter-sdk-image:latest as build

# create the flutteruser and group
RUN groupadd flutteruser && useradd -g flutteruser flutteruser

WORKDIR /app

COPY . .

# Configure Git as safe for Flutter (run as root)
RUN git config --global --add safe.directory /home/mobiledevops/.flutter-sdk

RUN flutter clean && dart pub cache clean

RUN chown -R flutteruser:flutteruser /app /home/mobiledevops/.flutter-sdk /home/mobiledevops/.pub-cache

USER flutteruser

RUN flutter pub get

RUN flutter build web

FROM nginx:stable-alpine

# copy to Nginx-Directory
COPY --from=build /app/build/web /usr/share/nginx/html

# own Nginx-Konfiguration 
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8081

# start Nginx-Webserver  
CMD ["nginx","-g", "daemon off;"]
