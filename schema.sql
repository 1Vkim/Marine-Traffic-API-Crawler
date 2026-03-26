-- SQL schema for storing vessel positions
CREATE TABLE vessel_positions (
    id SERIAL PRIMARY KEY,
    ship_name VARCHAR(255),
    time_stamp TIMESTAMPTZ DEFAULT NOW(),
    mmsi BIGINT NOT NULL,
    speed DOUBLE PRECISION NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL
);