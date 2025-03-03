from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def setpassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkpassword(self, password):
        return check_password_hash(self.password_hash, password)  # Use self.password_hash instead of self.password

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    mood = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint('username', 'date', name='unique_user_date'),)  # Ensures one entry per day


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')  # This renders the index page


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Handle login submission
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.checkpassword(password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")  

    return render_template('login.html')  # Fix: Show `login.html` for GET requests
  # Ensure the function always returns a response
  # Renders the login page when accessed with GET
# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        today = datetime.utcnow().date()
        existing_mood = Mood.query.filter_by(username=session['username'], date=today).first()

        if existing_mood:  # If the user already submitted their mood today
            return render_template('dashboard.html', username=session['username'])
        else:
            return redirect(url_for('mood_rating'))  # Redirect to mood rating page

    return redirect(url_for('index'))



# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', error="User already exists!")  
        else:
            new_user = User(username=username)
            new_user.setpassword(password)
            db.session.add(new_user)
            db.session.commit()
    return render_template('register.html')  # Return register page for GET requests

# LOGOUT
@app.route('/logout')
def logout():
    if "username" in session:
        session.pop('username', None)
        return redirect(url_for('index'))
    

@app.route('/mood_rating', methods=['GET', 'POST'])
def mood_rating():
    if 'username' not in session:
        return redirect(url_for('index'))  # If not logged in, go to home

    if request.method == 'POST':
        mood = request.form['mood']
        today = datetime.utcnow().date()

        # Check if the user has already submitted a mood today
        existing_mood = Mood.query.filter_by(username=session['username'], date=today).first()
        if not existing_mood:
            new_mood = Mood(username=session['username'], date=today, mood=mood)
            db.session.add(new_mood)
            db.session.commit()

        return redirect(url_for('dashboard'))  # Redirect to dashboard after submitting

    return render_template('moodrating.html')

@app.route('/journal',methods=['GET','POST']) 
def journal():
    return render_template('journal.html')


@app.route('/academic',methods=['GET','POST'])
def academic():
    return render_template('academic.html')





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
