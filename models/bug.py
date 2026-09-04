from datetime import datetime

from models import db


class Bug(db.Model):

    __tablename__ = "bugs"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    description = db.Column(
        db.Text,
        nullable=False
    )


    status = db.Column(
        db.String(50),
        default="Open",
        nullable=False
    )


    priority = db.Column(
        db.String(50),
        default="Medium",
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # User who owns this bug
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    # Analysis report this bug belongs to.
    # NULL means it is a manually created bug.
    analysis_id = db.Column(
        db.Integer,
        db.ForeignKey("analysis_reports.id"),
        nullable=True
    )


    def __repr__(self):

        return f"<Bug {self.title}>"