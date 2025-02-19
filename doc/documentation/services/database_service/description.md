### Description of the Database Service

The Database Service serves as interface to the database, it sends and receives data from and to the database. Data is received from the Detection Service [http_request_service.py](../../../../source/detectionService/app/service/http_request/http_request_service.py). The Data is then send to the Mailing Service and the Stock-Tracker app, after the changes have been saved in the database. Detection Service and Stock-Tracker app communicate via api interface which is specified here [api_specification.yml](api_specification.yml). Communication with the Mailing Service is done via its interface[api.py](../../../../source/mailingService/app/api/boundary/api.py). 

The Database Service API offers the following interfaces:
1. **Initializing or updating Products:** Everytime new data is received from the Detection Service, the Database Service determins if the request is ment to intitalize new products in the database or if it is just an udpate. The data is then handled accordingly. If successfully handled the Mailing Service is triggered to inform the user via an e-mail of the changes.

2. **Updating the App:** The App will trigger an update periodically via the "update_app" interface of the Database Service api. Which will send all data from the database when triggered.

3. **Healthcheck:** The healthcheck was implemented to make sure that docker compose will wait until the Database Service container is fully available, bevor starting Detection and Stock Tracker app. The healthcheck is triggered every 5 seconds to ensure its up and running.

The Database Service is modular designed. Its main components include:
- **[API](../../../../source/databaseService/app/api/boundary/api.py):** A simple FastAPI interface that processes and validates incoming requests.
- **[Buisness Facade](../../../../source/databaseService/app/api/control/api_bf.py):** Responsible for calling database_service methods and triggering Mailing Service.
- **[Database Service](../../../../source/databaseService/app/bm/database_service.py):** Responsible for the communication with the database. It initializes, updates, deletes and gets data.
- **[Database Provider](../../../../source/databaseService/app/database/database_provider.py):** Provides the necessary objects for communication with the database.

Additional components:
- **[Mailing Trigger](../../../../source/databaseService/app/api/control/mailing_trigger.py):** Responsible for preparing the message for the Mailing Service and sending it to the right interface.
- **[Database Tables](../../../../source/databaseService/app/database/database_table_modells.py):** Provides objects that represent the tables from the database.
- **[Models](../../../../source/databaseService/app/entities/models.py):** Provides all classes needed for communication with other Services. The models inherit from the BaseModel of the pydantic library, this ensures that all requests are validatet.
- **[Main](../../../../source/databaseService/app/main.py):** Serves as the entrypoint for the Database Service project.

(The project was created with the help of LLMs mainly ChatGPT)