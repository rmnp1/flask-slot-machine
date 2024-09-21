from crypt import methods

from flask import request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user

from flaskr.models import User

def register_routes(app, db, bcrypt):

    @app.route("/")
    def index():
        return render_template('index.html')


    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template('auth/signup.html')
        elif request.method == "POST":
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

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return 'Failed'

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

            current_user.deposit = current_user.deposit + deposit

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

            return render_template('lot/result.html', message=f"You bet {session['bet']}$ on {session['line']} lines")



