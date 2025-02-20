### Description of the Database

Tables
**Products:** 
    **- id** 
        Is the primary key of this table and is managed by the database system itself. The only time it will be changed by the Database Service is when new products are initialized.
    **- type_id**
        Is the id given by the Detection Service. Is used by the services to identify products.
    **- name**
        Is the name of the product (e.x. Bottle).
    **- picture**
        A base64-encoded string representing an image. The image is decoded and displayed in the app, showing all products. A box will be drawn around the products associated with this type_id that were detected the last time their quantity changed.
    **- amount**
        Represents ho many times a product has been currently detected.

**Overall Picture**
    **- id**    
        Is the primary key of this table and is managed by the database system itself. The only time it will be changed by the Databse Service is when new products are initialized.
    **- picture**
        A base64-encoded string representing an image. The image is decoded and displayed in the app, showing all products as they appeared when the last product was added or removed.