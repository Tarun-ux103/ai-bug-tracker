from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.bug import Bug
from models.analysis_report import AnalysisReport


main = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home():

    return render_template(
        "index.html"
    )


# Public dashboard
@main.route("/dashboard")
def dashboard():

    # All bugs are publicly visible
    bugs = Bug.query.order_by(
        Bug.created_at.desc()
    ).all()


    # Statistics for all bugs
    total_bugs = Bug.query.count()


    open_bugs = Bug.query.filter_by(
        status="Open"
    ).count()


    in_progress_bugs = Bug.query.filter_by(
        status="In Progress"
    ).count()


    resolved_bugs = Bug.query.filter_by(
        status="Resolved"
    ).count()


    # AI reports are private
    grouped_reports = []


    if current_user.is_authenticated:

        analysis_reports = AnalysisReport.query.filter_by(
            user_id=current_user.id
        ).order_by(
            AnalysisReport.created_at.desc()
        ).all()


        for report in analysis_reports:

            report_bugs = Bug.query.filter_by(
                analysis_report_id=report.id,
                user_id=current_user.id
            ).order_by(
                Bug.created_at.desc()
            ).all()


            issues = report.issues or []


            critical_count = 0
            high_count = 0
            medium_count = 0
            low_count = 0


            for issue in issues:

                severity = issue.get(
                    "severity",
                    ""
                ).lower()


                if severity == "critical":
                    critical_count += 1

                elif severity == "high":
                    high_count += 1

                elif severity == "medium":
                    medium_count += 1

                elif severity == "low":
                    low_count += 1


            grouped_reports.append({

                "report": report,

                "bugs": report_bugs,

                "issues_count": len(issues),

                "saved_bugs_count": len(report_bugs),

                "critical_count": critical_count,

                "high_count": high_count,

                "medium_count": medium_count,

                "low_count": low_count

            })


    return render_template(
        "dashboard.html",

        bugs=bugs,

        grouped_reports=grouped_reports,

        total_bugs=total_bugs,

        open_bugs=open_bugs,

        in_progress_bugs=in_progress_bugs,

        resolved_bugs=resolved_bugs
    )


@main.route(
    "/create-bug",
    methods=["GET", "POST"]
)
@login_required
def create_bug():

    if request.method == "POST":

        title = request.form.get("title")

        description = request.form.get("description")

        priority = request.form.get("priority")


        new_bug = Bug(
            title=title,
            description=description,
            priority=priority,
            user_id=current_user.id
        )


        try:

            db.session.add(new_bug)

            db.session.commit()


            flash(
                "Bug reported successfully!",
                "success"
            )


            return redirect(
                url_for("main.dashboard")
            )


        except Exception:

            db.session.rollback()


            flash(
                "Error saving bug. Please try again.",
                "error"
            )


            return redirect(
                url_for("main.create_bug")
            )


    return render_template(
        "create_bug.html"
    )


# Public bug details
@main.route("/bug/<int:bug_id>")
def bug_details(bug_id):

    bug = Bug.query.get_or_404(
        bug_id
    )


    return render_template(
        "bug_details.html",
        bug=bug
    )


@main.route(
    "/bug/<int:bug_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_bug(bug_id):

    bug = Bug.query.get_or_404(
        bug_id
    )


    # Only the creator can edit
    if bug.user_id != current_user.id:

        abort(403)


    if request.method == "POST":

        bug.title = request.form.get("title")

        bug.description = request.form.get("description")

        bug.priority = request.form.get("priority")

        bug.status = request.form.get("status")


        db.session.commit()


        flash(
            "Bug updated successfully!",
            "success"
        )


        return redirect(
            url_for(
                "main.bug_details",
                bug_id=bug.id
            )
        )


    return render_template(
        "edit_bug.html",
        bug=bug
    )


@main.route(
    "/bug/<int:bug_id>/delete",
    methods=["POST"]
)
@login_required
def delete_bug(bug_id):

    bug = Bug.query.get_or_404(
        bug_id
    )


    # Only the creator can delete
    if bug.user_id != current_user.id:

        abort(403)


    db.session.delete(bug)

    db.session.commit()


    flash(
        "Bug deleted successfully!",
        "success"
    )


    return redirect(
        url_for("main.dashboard")
    )