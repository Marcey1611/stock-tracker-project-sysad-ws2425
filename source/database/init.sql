CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_picture VARCHAR(255),
    product_name VARCHAR(255),
    product_amount BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS overall_picture (
    overall_picture_id SERIAL PRIMARY KEY,
    overall_picture VARCHAR(255)
)