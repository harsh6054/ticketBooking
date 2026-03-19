🎬 Movie Ticket Booking System

A Movie Ticket Booking System built using Python (Tkinter GUI) and MySQL database.
This desktop-based application allows users to view movies, select showtimes, book tickets, and manage reservations efficiently.

🚀 Features

🎞️ View available movies and show timings
🎟️ Book, update, or cancel movie tickets
👥 Manage customer information
💾 Stores data securely in MySQL database
💻 Simple and user-friendly Tkinter GUI
🔍 Search and filter bookings easily

🛠️ Technologies Used
Category	Technology
Frontend (GUI)	Python Tkinter
Backend	Python
Database	MySQL
Connector	pymysql
IDE (optional)	VS Code / PyCharm

⚙️ Installation and Setup
1. Install dependencies :
pip install pymysql

2. Set up MySQL database:

Open MySQL Workbench or Command Prompt

Create a database (for example):

CREATE DATABASE movie_db;


Import the provided SQL file if available (e.g., movie_db.sql)

Update your database connection in db_config.py:

host = "localhost"
user = "root"
password = "yourpassword"
database = "movie_db"

4️⃣ Run the app
python main.py


	
	
🧠 Future Improvements

Add user login and authentication

Implement online payment integration

Email ticket confirmation feature

Add movie poster & trailer previews

🧑‍💻 Author

Harshvardhan Patil
📧 [harshpatil6054@gmail.com]



