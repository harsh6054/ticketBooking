create table movies(show_no varchar(20), show_time varchar(20),movie_name varchar(25),price int(8),seats int(10));
insert into movies(show_no,show_time,movie_name,price,seats) values('First','3pm - 5.30pm','Venom',150,20);
CREATE TABLE movies.bookings (id INT AUTO_INCREMENT PRIMARY KEY,show_no VARCHAR(20),customer_name VARCHAR(50),row_no INT,seat_no INT);
