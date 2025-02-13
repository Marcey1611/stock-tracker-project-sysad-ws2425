### Description of the Mailing Service

The Mailing Service is responsible for sending automated emails based on the information provided by the DatabaseService. It is accessed via a REST interface and performs the following functions:

1. **Processing Product Changes:** The service receives information about changes in a shelf, such as when products are added or removed. This data is validated and prepared for email creation.

2. **Sending Status Emails:** Based on the provided data, the service generates emails to inform about product changes. These emails are sent via a Gmail account to a predefined address.

3. **Error Notifications:** In case of invalid data or other issues, the service generates error messages which are returned to the DatabaseService. Additionally, the service has a dedicated interface allowing the DatabaseService to notify the Mailing Service if an error occurs in one of the other services. The Mailing Service then sends an email containing the error details.

The Mailing Service is modular in design. Its main components include:
- **API:** The interface that processes and validates incoming requests.
- **Business Facade (ApiBF):** Responsible for preparing the data for email creation.
- **Mailing Logic (MailSendingServiceBA):** Manages the actual email sending, including configuration and message dispatch.

(Partially generated with ChatGPT)
