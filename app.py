from flask import Flask, render_template, request, redirect, flash
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Database connection
def get_db_connection():
    return pyodbc.connect(app.config['DATABASE_CONNECTION'])

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM Users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    connection.close()
    
    if user_data:
        return User(user_data.id, user_data.username)
    return None

# Redirect root route to login if user is not authenticated
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/index')
    return redirect('/login')

# Index route to view tasks, protected by login_required
@app.route('/index')
@login_required
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description FROM Tasks")
    tasks = cursor.fetchall()
    connection.close()
    
    return render_template('index.html', tasks=tasks)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'danger')
                return redirect('/register')

            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
            connection.commit()
            flash('Registration successful! You can log in now.', 'success')
            return redirect('/login')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            connection.rollback()
        finally:
            connection.close()
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id, password FROM Users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data and check_password_hash(user_data.password, password):
                user = User(user_data.id, username)
                login_user(user)
                flash('Login successful!', 'success')
                return redirect('/index')
            else:
                flash('Invalid username or password.', 'danger')
        finally:
            connection.close()

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect('/login')

# Add task route
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Tasks (title, description) VALUES (?, ?)", (title, description))
            connection.commit()
            flash('Task added successfully!', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
            connection.rollback()
        finally:
            connection.close()
        return redirect('/index')
    
    return render_template('form.html', task=None)

# Fetch task route
@app.route('/task/<int:id>')
@login_required
def fetch_task(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description FROM Tasks WHERE id = ?", (id,))
    task = cursor.fetchone()
    connection.close()

    if task:
        return render_template('task_detail.html', task=task)
    else:
        flash('Task not found!', 'danger')
        return redirect('/index')

# Edit task route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, title, description FROM Tasks WHERE id = ?", (id,))
    task = cursor.fetchone()

    if not task:
        flash("Task not found!", "danger")
        return redirect('/index')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        try:
            cursor.execute("UPDATE Tasks SET title = ?, description = ? WHERE id = ?", (title, description, id))
            connection.commit()
            flash('Task updated successfully!', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
            connection.rollback()
        finally:
            connection.close()
        return redirect('/index')
    
    connection.close()
    return render_template('form.html', task=task)

# Delete task route
@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("DELETE FROM Tasks WHERE id = ?", (id,))
        connection.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash(f"An error occurred: {e}", 'danger')
        connection.rollback()
    finally:
        connection.close()
    
    return redirect('/index')

if __name__ == '__main__':
    app.run(debug=True)
