-- Set the character set and collation for the session
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

CREATE SCHEMA IF NOT EXISTS numerical_methods_api DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE numerical_methods_api;

-- Create the users table
CREATE TABLE IF NOT EXISTS numerical_methods_api.users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

