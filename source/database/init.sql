CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    picture VARCHAR(255),
    amount BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS overall_picture (
    id SERIAL PRIMARY KEY,
    picture VARCHAR(255)
)