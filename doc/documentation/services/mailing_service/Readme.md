# Description of the Mailing Service

The Mailing Service is responsible for sending automated emails based on the information provided by the DatabaseServices [mailing trigger](../../../../source/databaseService/app/api/control/mailing_trigger.py). Therefore the service contains an api which is specified in the [api spec](./api_specification.yml). In the same directory as the api spec you can find an [class diagram](./class_diagram.puml) and a [sequence diagram](./sequence_diagram.puml). It is accessed via REST interfaces and performs the following functions.

## Functions of the Mailing Service

1. **Processing Product Changes:** The service receives information about changes of products, such as when products are added or removed. This data is validated and prepared for email creation. This data will be saved in a list. All two minutes a email will be sent if new data of changes are available.

2. **Sending Update Emails:** Based on the provided data, the service generates emails to inform about product changes. These emails are sent via a Gmail account to a predefined address.

3. **Error Notifications:** In case of invalid data or other issues, the service generates error messages which are returned to the DatabaseService. Additionally, the service has a dedicated interface allowing the DatabaseService to notify the Mailing Service if an error occurs in one of the other services. The Mailing Service then sends an email containing the error details.

## Components

### Main Components

The Mailing Service is modular in design. Its main components include:
- **[API](../../../../source/mailingService/app/api/boundary/api.py):** The interface that processes and validates incoming requests, it works with FastAPI. 
- **[Business Facade](../../../../source/mailingService/app/api/control/api_bf.py):** Responsible for preparing the data for email creation.
- **[Mail Preparing](../../../../source/mailingService/app/bm/mail_preparing_service_ba.py):** Manages the preparing of the mailing data. Also handles a delayed sending of update emails. Because if some product amounts are updated sucessively we shouldnt send an email each update, because that would be to much emails. So the MailPreparingServiceBA saves the updates and just sends maximum one email all two minutes.
- **[Mail Sending](../../../../source/mailingService/app/bm/mail_sending_service_ba.py):** Manages the actual email sending.

### Additional Components

Futhermore there are some additional components:
- **[Exception Handler](../../../../source/mailingService/app/api/boundary/exception_handler.py):** A simple FastAPI exception handler which handle the two custom exceptions and all other exceptions and comunicates these exceptions to the outside.
- **[Action Enum](../../../../source/mailingService/app/entity/enums/):** Enum with the values CHANGED and DELETED which seperates the the two different types of emails sent by this service.
- **[Internal Error Exception](../../../../source/mailingService/app/entity/exceptions/internal_error_exception.py):** Custom exception for errors at the client side.
- **[Models for the mailing data](../../../../source/mailingService/app/entity/models/mail_data.py):** Two models, one for the update and one for the error mails. Among other things, these models are used for validation which is possible because of the use of FastAPI.

### Requirements and additional Files

There are some more files which are used from the MailingService:
- **Update [Email HTML Template](../../../../source/mailingService/app/email_template.html) and [Error Email HTML Template](../../../../source/mailingService/app/error_email_template.html):** There are also two html templates that the emails sent by the service looking good. For the better lookingf there is also a [logo](../../../../source/mailingService/app/logo.png) in each email.
- **[main.py](../../../../source/mailingService/app/main.py):** The main python file of the project.
- **[requirements.txt](../../../../source/mailingService/requirements.txt):** Here are the requirements which are needed and will be installed by docker. These requirements are:
  - [fastapi](https://github.com/fastapi/fastapi): FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
  - [uvicorn](https://github.com/encode/uvicorn): Uvicorn is an ASGI web server implementation for Python.
  - [pydantic](https://github.com/pydantic/pydantic): Data validation using Python type hints.
  - [requests](https://github.com/psf/requests): Requests is a simple, yet elegant, HTTP library.
  - [pydantic](https://github.com/pallets/jinja): Jinja is a fast, expressive, extensible templating engine.
  - [python-dotnev](https://github.com/theskumar/python-dotenv): Python-dotenv reads key-value pairs from a .env file and can set them as environment variables.
- **[Dockerfile](../../../../source/mailingService/Dockerfile):** Finally there is a docker file for the mailing-service.

## Setting up the receiver Mail-Address

The email to which the update/error mails are sent can be set in the [mailing service docker-compose file](../../../../source/mailingService/docker-compose.yml). The smtp server and port, in our case gmail, and also the mail address with which the emails should be sent and the password for its mail-account can also be set in this docker-compose file.
