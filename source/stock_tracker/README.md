# stock_tracker

In order to fully edit the Flutter website, 
it is a prerequisite to have Flutter properly installed on the computer. 

The docker container only represents the representation.

Small changes are possible in the (name).dart files, then the following commands must be executed:

- <code>docker-compose down -v</code>
- <code>docker-compose build</code>
- <code>docker-compose up</code>


if you want to use a different port instead of 40105:
Changes need to be made in...

api_config.dart -> localhost:40105                   | change port
nginx.conf -> listen 40105;                          | change port
docker-compose.yml -> ports: - "40105:40105"          | change ports
dockerfile (stock_tracker) -> EXPOSE 40105           | change port
docker-compose.yml (source) -> ports: - "40105:40105" | change ports