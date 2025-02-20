# Project Requirements

## General Goals
Our goal is to track what is inside a shelf (fridge) and determine what has been added or removed.

## Must-Have Requirements

### Detection (Implemented)
- A product must be identified using a camera, and the correct product must be recognized. 

### Storage (Implemented)
- The data should be stored in a database and be retrievable. 

### Event Handling (Implemented)
- After an action (adding/removing a product), the user should receive an email with the updated product list. 

## Should-Have Requirements

### Web Interface
- A website or an app should display the current inventory. (Implemented both)
- Additional the website/app should show a history. (Not Implemented)

### Confirmation (Not implemented)
- An LED on the camera should light up when the system correctly recognizes a product. 

## Nice-to-Have Requirements

### Advanced Detection (Not implemented)
- Use an additional camera to detect whether a product is being added or removed.
- Recognize how much of a product has already been consumed.

### Home Assistant Integration (Not implemented)
- A **Home Assistant** Docker container.
- A list or entity in this container to track the products.
