CREATE TABLE IF NOT EXISTS Products (
    productId SERIAL PRIMARY KEY,
    productName VARCHAR(255),
    productAmount NUMBER(20) NOT NULL
);