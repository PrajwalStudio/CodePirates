from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import logging
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database location
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('login.html')  # Replace with your homepage template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        start_time = datetime.now()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        end_time = datetime.now()
        logger.info(f"Signup query took {end_time - start_time} seconds")

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        start_time = datetime.now()
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        end_time = datetime.now()
        logger.info(f"Login query took {end_time - start_time} seconds")

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

def open_browser():
    webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open("http://127.0.0.1:5000")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)