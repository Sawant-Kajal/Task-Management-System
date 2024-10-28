# Task-Management-System

This is a simple task management application built with Flask, allowing users to register, log in, and manage their tasks. Users can create, edit, and delete tasks, with all data stored in a SQL database.

## Features

- User registration and login system with password hashing.
- View a list of tasks.
- Add new tasks with titles and descriptions.
- Edit existing tasks.
- Delete tasks.
- User authentication to ensure secure access.

## Technologies Used

- **Python**: The programming language for backend development.
- **Flask**: A micro web framework for building web applications.
- **Flask-Login**: For user session management.
- **pyodbc**: For connecting to SQL databases.
- **HTML/CSS**: For front-end development.
- **Bootstrap**: For responsive design.

## Prerequisites

- Python 3.x
- A SQL database (e.g., SQL Server) with a connection string to be used in the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-management-app.git
   cd task-management-app


2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
2.1 Install the required packages:

```bash
pip install Flask Flask-Login pyodbc werkzeug
```

2.2 Configure your database connection in the config.py file. The connection string should look something like this:

python
```bash
class Config:
    DATABASE_CONNECTION = 'Driver={SQL Server};Server=your_server;Database=your_database;UID=your_username;PWD=your_password;'
```
Database Setup
Before running the application, you need to set up the database. Create the following tables:

sql
```bash
CREATE TABLE Users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(100) NOT NULL
);

CREATE TABLE Tasks (
    id INT PRIMARY KEY IDENTITY(1,1),
    title NVARCHAR(100) NOT NULL,
    description NVARCHAR(255) NOT NULL
);
```
3. Usage
Run the application:

```bash

python app.py
```
Open your web browser and go to http://127.0.0.1:5000/ to access the application.

You will be redirected to the login page. From there, you can register a new user account or log in with existing credentials.
