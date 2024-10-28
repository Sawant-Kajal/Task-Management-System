from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from config import Config

app = Flask(__name__)
app.config.from_object(Config)



def get_db_connection():
    connection = pyodbc.connect(app.config['DATABASE_CONNECTION'])
    return connection
# Connect to the database
connection = get_db_connection()
cursor = connection.cursor()

# Fetch all records from the Tasks table
cursor.execute("SELECT title, description FROM Tasks")
tasks = cursor.fetchall()
connection.close()

# Reindex tasks
reindexed_tasks = [(index + 1, task[0], task[1]) for index, task in enumerate(tasks)]

# Display the results
print("id\tTitle\t\tDescription")
for task in reindexed_tasks:
    print(f"{task[0]}\t{task[1]}\t{task[2]}")
