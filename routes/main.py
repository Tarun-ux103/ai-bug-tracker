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


main = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home():

    return render_template(
        "index.html"
    )


@main.route("/dashboard")
@login_required
def dashboard():

    bugs = Bug.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Bug.created_at.desc()
    ).all()


    total_bugs = Bug.query.filter_by(
        user_id=current_user.id
    ).count()


    open_bugs = Bug.query.filter_by(
        user_id=current_user.id,
        status="Open"
    ).count()


    in_progress_bugs = Bug.query.filter_by(
        user_id=current_user.id,
        status="In Progress"
    ).count()


    resolved_bugs = Bug.query.filter_by(
        user_id=current_user.id,
        status="Resolved"
    ).count()


    return render_template(
        "dashboard.html",
        bugs=bugs,
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

        title = request.form.get(
            "title"
        )

        description = request.form.get(
            "description"
        )

        priority = request.form.get(
            "priority"
        )


        new_bug = Bug(
            title=title,
            description=description,
            priority=priority,
            user_id=current_user.id
        )


        try:

            db.session.add(
                new_bug
            )

            db.session.commit()


            flash(
                "Bug reported successfully!",
                "success"
            )


            return redirect(
                url_for(
                    "main.dashboard"
                )
            )


        except Exception:

            db.session.rollback()


            flash(
                "Error saving bug. Please try again.",
                "error"
            )


            return redirect(
                url_for(
                    "main.create_bug"
                )
            )


    return render_template(
        "create_bug.html"
    )


@main.route(
    "/bug/<int:bug_id>"
)
@login_required
def bug_details(bug_id):

    bug = Bug.query.filter_by(
        id=bug_id,
        user_id=current_user.id
    ).first_or_404()


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


    if bug.user_id != current_user.id:

        abort(
            403
        )


    if request.method == "POST":

        bug.title = request.form.get(
            "title"
        )

        bug.description = request.form.get(
            "description"
        )

        bug.priority = request.form.get(
            "priority"
        )

        bug.status = request.form.get(
            "status"
        )


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


    if bug.user_id != current_user.id:

        abort(
            403
        )


    db.session.delete(
        bug
    )

    db.session.commit()


    flash(
        "Bug deleted successfully!",
        "success"
    )


    return redirect(
        url_for(
            "main.dashboard"
        )
    )