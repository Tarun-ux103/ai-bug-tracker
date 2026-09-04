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

    # Connect this bug to an analysis report
    analysis_report_id = db.Column(
        db.Integer,
        db.ForeignKey("analysis_reports.id"),
        nullable=True
    )

    # Connect this bug to a user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):

        return f"<Bug {self.title}>"