from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db


class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )


    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )


    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    # Manual and AI-generated bugs
    bugs = db.relationship(
        "Bug",
        backref="creator",
        lazy=True
    )


    # AI analysis reports created by this user
    analysis_reports = db.relationship(
        "AnalysisReport",
        backref="creator",
        lazy=True,
        cascade="all, delete-orphan"
    )


    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


    def __repr__(self):

        return f"<User {self.username}>"