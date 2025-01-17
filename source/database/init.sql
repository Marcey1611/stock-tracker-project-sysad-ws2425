CREATE TABLE IF NOT EXISTS products (
    productId SERIAL PRIMARY KEY,
    product_picture VARCHAR(255),
    productName VARCHAR(255),
    productAmount NUMBER(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS overall_picture (
    overall_picture VARCHAR(255),
)