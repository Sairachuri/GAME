from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/harshdb'  # Replace with your MySQL connection details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    data = db.Column(db.String(255), default='Default data')

# Create the database tables
db.create_all()

# Dummy session data to store user login status
session = {}


# Sample user data for demonstration purposes
users = {
    'user1': {'password': 'password1', 'data': 'Page data for user1'},
    'user2': {'password': 'password2', 'data': 'Page data for user2'},
}

# Dummy session data to store user login status
session = {}


@app.route('/')
def home():
    username = session.get('username')
    if username:
        user_data = users.get(username, {}).get('data', 'Default data')
        return render_template('edit_page.html', username=username, user_data=user_data)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
