CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXIST timescaledb;

CREATE TABLE vessel_positions (
    time TIMESTAMPTZ NOT NULL,
    mmsi BIGINT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('vessel_positions', 'time');