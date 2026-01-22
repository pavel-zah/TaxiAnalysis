CREATE DATABASE taxi;

\c taxi

CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    register_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    license_plate VARCHAR(50) NOT NULL,
    register_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rides (
    id VARCHAR(255) PRIMARY KEY,
    driver_id VARCHAR(255) NOT NULL,
    rider_id VARCHAR(255) NOT NULL,
    starting_point VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    tip DECIMAL(10, 2) NOT NULL DEFAULT 0.00,

    CONSTRAINT fk_rides_driver
        FOREIGN KEY (driver_id)
        REFERENCES drivers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_rides_rider
        FOREIGN KEY (rider_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);