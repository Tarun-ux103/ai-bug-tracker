from datetime import datetime

from models import db


class AnalysisReport(db.Model):

    __tablename__ = "analysis_reports"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    language = db.Column(
        db.String(100),
        nullable=False
    )


    source_code = db.Column(
        db.Text,
        nullable=False
    )


    summary = db.Column(
        db.Text,
        nullable=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    bugs = db.relationship(
        "Bug",
        backref="analysis_report",
        lazy=True,
        cascade="all, delete-orphan"
    )


    def __repr__(self):

        return f"<AnalysisReport {self.title}>"