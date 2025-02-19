CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    type_id INTEGER,
    name VARCHAR(255),
    picture TEXT,
    amount BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS overall_picture (
    id SERIAL PRIMARY KEY,
    picture TEXT
)