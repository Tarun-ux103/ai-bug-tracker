from flask import Flask
from flask_login import LoginManager

from config import Config
from models import db

from models.user import User
from models.bug import Bug

from routes.main import main
from routes.auth import auth
from routes.analyzer import analyzer_bp


def create_app():

    # Create Flask application
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)


    # Safe database diagnostics
    database_uri = app.config.get(
        "SQLALCHEMY_DATABASE_URI"
    )

    print(
        "ACTIVE DATABASE CONFIGURED:",
        bool(database_uri)
    )


    if database_uri:

        # Do not print password
        safe_database_uri = database_uri.split(
            "@"
        )[-1]

        print(
            "ACTIVE DATABASE:",
            safe_database_uri
        )


    # Initialize SQLAlchemy
    db.init_app(app)


    # Initialize Flask-Login
    login_manager = LoginManager()

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"


    # Load logged-in user
    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )


    # Register blueprints
    app.register_blueprint(main)

    app.register_blueprint(auth)

    app.register_blueprint(analyzer_bp)


    # Create database tables if they don't exist
    with app.app_context():

        db.create_all()


    return app


# Required for Vercel
app = create_app()


# Local development
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )