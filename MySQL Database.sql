CREATE DATABASE password_manager;

USE password_manager;

CREATE TABLE password_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);