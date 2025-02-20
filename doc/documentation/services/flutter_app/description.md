#Description of the StockTrackerApp

StockTracker is a mobile application and website developed with Flutter and Dart. It is used to monitor inventory levels by retrieving data from a database via an API interface and presenting it clearly. The app offers an easy way to view the current status of existing products.

Features

Display of inventory: The app shows all products stored in the database.

Automatic update: The data is updated at regular intervals to always provide up-to-date information.

Navigation through the app: Users can switch between different views, for example to view inventory or a history (not yet implemented).

Architecture

The app consists of several core components:

API configuration (ApiConfig********************): Defines the base URL of the API that is used to query data.

API service (ApiService********************): Provides methods to retrieve and process the API data.

Data display (StockDataTableWidget********************): Displays the inventory data in tabular form.

Homepage (HomePage********************): Contains the main navigation and redirects users to the inventory overview or future additional functions.

Main application (StockTrackerApp********************): Initializes the app and loads the home page.

Using the app

Installing and starting the application

APK installation on Android devices:

Download the StockTracker.apk.

Install the file on your Android device (you may need to allow "unknown sources").

Open the app after installation.

Starting the web version:

Go to the website where the application is hosted.

If this is run locally, use: <localhost:40105>

The data is loaded and displayed automatically.

Using the app

After starting the app or website, the current inventory is automatically retrieved from the API.

You can switch between different views using the navigation.

The data updates automatically every 10 seconds.

If there are images of the products, these will be displayed.

Using the StockTracker.apk (release version)

If you are using the app as a .apk release file, follow these steps:

Install: Download the APK to your Android device and install it.

API connection: Make sure that your device is on the same network as the server on which the API is running.

Troubleshooting:

If no data is displayed, check whether the API is accessible (e.g. via website).

Make sure that your device has an active internet connection.

Technical details

Programming language: Dart (Flutter)

Backend connection: REST API

UI framework: Flutter widgets

API calls: http package

Data processing: JSON parsing

Error messages: console output with logger