-- Create database
CREATE DATABASE IF NOT EXISTS rec;
USE rec;

-- Drop old tables
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS seats;
DROP TABLE IF EXISTS movie;

-- Movies table
CREATE TABLE movie (
    show_no INT PRIMARY KEY,
    show_time VARCHAR(50),
    movie_name VARCHAR(100),
    price INT,
    total_seats INT
);

-- Insert sample movies
INSERT INTO movie (show_no, show_time, movie_name, price, total_seats) VALUES
(1, '10:00 AM', 'Avengers', 200, 10),
(2, '1:00 PM', 'Inception', 180, 10),
(3, '4:00 PM', 'Interstellar', 220, 10);

-- Seats table
CREATE TABLE seats (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    show_no INT,
    seat_no VARCHAR(10),
    status ENUM('available','booked') DEFAULT 'available',
    FOREIGN KEY (show_no) REFERENCES movie(show_no)
);

-- Insert 10 seats per show
INSERT INTO seats (show_no, seat_no) VALUES
(1,'A1'),(1,'A2'),(1,'A3'),(1,'A4'),(1,'A5'),
(1,'B1'),(1,'B2'),(1,'B3'),(1,'B4'),(1,'B5'),
(2,'A1'),(2,'A2'),(2,'A3'),(2,'A4'),(2,'A5'),
(2,'B1'),(2,'B2'),(2,'B3'),(2,'B4'),(2,'B5'),
(3,'A1'),(3,'A2'),(3,'A3'),(3,'A4'),(3,'A5'),
(3,'B1'),(3,'B2'),(3,'B3'),(3,'B4'),(3,'B5');

--Bookings table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    show_no INT,
    seat_no VARCHAR(10),
    price INT,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (show_no) REFERENCES movie(show_no)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


