CREATE TABLE IF NOT EXISTS Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS StockLog (
    ProductID INTEGER REFERENCES Products(ProductID),
    SystemTimeIN TIME,
    SystemTimeOUT TIME
);