CREATE TABLE IF NOT EXISTS products (
    productId SERIAL PRIMARY KEY,
    productName VARCHAR(255),
    productAmount BIGINT NOT NULL
);