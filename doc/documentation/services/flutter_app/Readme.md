
### Description of the StockTrackerApp

StockTracker is a mobile application and website developed with Flutter and Dart. It is used to monitor inventory levels by retrieving data from a database via an API interface[api_config.dart](../../../../source/stock_tracker/lib/api_config.dart) and presenting it clearly. The app offers an easy way to view the current status of existing products.


**Features**

Display of inventory: The app shows all products stored in the database.

Automatic update: The data is updated at regular intervals to always provide up-to-date information.

Navigation through the app: Users can switch between different views, for example to view inventory or a history (not yet implemented).


**Architecture**

The app consists of several core components:

 [API Configuration](../../../../source/stock_tracker/lib/api_config.dart): Defines the base URL of the API that is used to query data.

 [API Service](../../../../source/stock_tracker/lib/api_service.dart): Provides methods to retrieve and process the API data.

 [Data Display](../../../../source/stock_tracker/lib/data_tables.dart): Displays the inventory data in tabular form.

 [Homepage](../../../../source/stock_tracker/lib/home_page.dart): Contains the main navigation and redirects users to the inventory overview or future additional functions.

 [Main Application](../../../../source/stock_tracker/lib/main.dart): Initializes the app and loads the home page.


**Using the StockTracker website**

The StockTracker website is used to display the current inventory data and is provided via a Docker container. In order for the website to function correctly, the IP address of the server on which the Docker container is running must be checked and adjusted if necessary.

Checking and adjusting the IP address

Before starting the website, the correct IP address of the container must be checked in two places and adjusted if necessary:

[API Configuration](../../../../source/stock_tracker/lib/api_config.dart): check or replace the IP address for "for web" and "for RealPhone"

[Nginx.conf](../../../../source/stock_tracker/nginx.conf): check or replace the IP address at server_name

If the IP address of the server has changed or is different from the previous configuration, these two places must be updated.

Starting and using the website

Make sure that the database service is started.

As soon as the container is running, the website is fully available.

The website and the app update automatically so that the inventory data is always up to date.

The application is now ready for use and always displays the latest inventory in the database.


**Using the app**

To install the StockTracker app on your Android smartphone, follow these steps:

Copy APK file to computer [StockTracker.apk](../../../../source/stock_tracker/apk_file/app-release.apk)

Make sure you do not modify or rename the file.

Transfer APK to smartphone

By email: Send the file as an attachment to your own email address and open the email on your smartphone.

By USB cable: Connect your smartphone to the computer and copy the APK file to any folder on the device.

By cloud storage: Upload the file to a cloud service (e.g. Google Drive, Dropbox) and download it to your smartphone.

Install APK on Android smartphone

Open the APK file on your smartphone.

If a security warning appears, enable the Allow unknown sources option under Settings > Security.

Follow the instructions on the screen and install the app.

Start and use the app

After successful installation, you will find the StockTracker app in the app menu of your smartphone.

Open the app and check the inventory data.

**Note: This app only works on Android devices. Installation on iOS (iPhone/iPad) is not possible.**


Troubleshooting:

API connection: Make sure that your device is on the same network as the server on which the API is running.

If no data is displayed, check whether the API is accessible (e.g. via website).

Make sure that your device has an active internet connection.


**Technical details**

Programming language: Dart (Flutter)

Backend connection: REST API

UI framework: Flutter widgets

API calls: http package

Data processing: JSON parsing

Error messages: console output with logger


**Limitations of making changes to the StockTracker website & app**

Small changes to the website or app are possible, but they are not testable without installing the necessary development tools and support is limited.

Tools required for major changes

To make more extensive changes and test the code before deployment, it is recommended to install the following tools:

Flutter SDK: For developing and customizing the app

Android Studio: For testing and debugging on Android devices and emulators

A suitable code editor (e.g. Visual Studio Code or IntelliJ IDEA)

Limitations without installation

Changes to the source code can only be made without direct testing.

The app and website cannot be run locally or checked for errors.

Functions that rely on API requests or Flutter-specific components cannot be validated.

For detailed installation instructions, see: [Insert link to installation instructions here]