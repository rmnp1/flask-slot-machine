from flask import Flask
from flask import redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import SECRET_KEY

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.secret_key = SECRET_KEY

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    # Unregistered user processing
    from .models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return redirect(url_for('page.index'))

    bcrypt.init_app(app)

    from .routes import page
    app.register_blueprint(page)

    # Initialize database migration tool
    migrate = Migrate(app, db, command='db')

    return app
