# How to database

Run the docker-start.bat file in the windows cmd or run the following commands:
- <code>docker-compose down</code>
- <code>docker-compose build</code>
- <code>docker-compose up</code>

Then you can use the following command in another terminal to get acces to the database:
- <code>docker exec -it stock_tracker_postgres_db psql -U myuser mydatabase</code>

Now you have access to the database and you can use sql-syntax to make whatever you want.