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

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)


    login_manager = LoginManager()

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"


    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )


    app.register_blueprint(main)

    app.register_blueprint(auth)

    app.register_blueprint(analyzer_bp)


    with app.app_context():

        db.create_all()


    return app


# This is important for Vercel
app = create_app()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )