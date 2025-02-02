from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask import request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
import random


db = SQLAlchemy()

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.secret_key = "SOME KEY"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    deposit = db.Column(db.Integer)
    role = db.Column(db.String)

    def __repr__(self):
        return f'Glad to see you again. Ready to play {self.username}?'

    def get_id(self):
        return self.uid

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('index'))

bcrypt = Bcrypt(app)



# Initialize database migration tool
migrate = Migrate(app, db, command='db')

# Register the slot machine values
symbols = ['🍒', '🍋', '🍊', '🍉', '⭐', '🔔']
symbol_value = { '🍒' : 6,
                 '🍋' : 4,
                 '🍊' : 3,
                 '🍉' : 2,
                 '⭐' : 3,
                 '🔔' : 1
                 }


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('auth/signup.html')
    elif request.method == "POST":
        # Creating new user in database
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter(User.username == username).first()

        # Check for existing of user
        if user is None:
            return "User not found. Sign in."

        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/deposit', methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "GET":
        return render_template('lot/deposit.html')
    elif request.method == "POST":
        deposit = int(request.form.get('deposit'))

        # Deposit update by user
        if current_user.deposit:
            current_user.deposit = current_user.deposit + deposit
        else:
            current_user.deposit = deposit

        db.session.commit()
    return redirect(url_for('index'))


@app.route('/play', methods=['GET', 'POST'])
@login_required
def play():
    if request.method == "GET":
        return render_template('lot/session.html')
    elif request.method == "POST":
        session['bet'] = int(request.form.get('bet'))
        session['line'] = int(request.form.get('line'))

        return redirect(url_for('result'))


@app.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    winnings = 0
    bet = session['bet']
    bet_line = session['line']
    total_bet = bet * bet_line
    info = symbol_value.items()

    if request.method == "GET":
        message = f"You bet ${bet} on {bet_line} lines. The total bet is: ${total_bet}. Now you can spin the slot machine or change your bet."
        return render_template('lot/result.html', message=message, info=info)
    elif request.method == "POST":
        total_bet = session['bet'] * session['line']
        slots = [[random.choice(symbols) for _ in range(3)] for _ in range(3)] # Random generation of slot machine values

        session['slots'] = slots
        winning_lines = []

        message = f"You bet {bet}$ on {bet_line} lines. Total bet is equal to: ${total_bet}"

        '''
        Check for winning lines in generated slot machine
        and the winnings are updated based on the symbol's 
        value multiplied by the bet amount.
        '''
        for index, line in enumerate(session['slots']):
            if all(x == line[0] for x in line):
                winning_lines.append(index + 1)
                winnings += symbol_value[line[0]] * bet

        if winning_lines:
            win_message = f"You won {winnings}$ on line: {', '.join(map(str, winning_lines))}"
        else:
            win_message = None

        # Adjust the user's deposit balance
        current_user.deposit = current_user.deposit - total_bet + winnings

        if current_user.deposit < total_bet:
            return render_template('lot/deposit.html', message="Your deposit is lower than your bet. Please deposit more to play.")

        db.session.commit() # Recording all changes made to the database

        return render_template('lot/result.html', slots=slots, message=message, win_message=win_message, info=info)

