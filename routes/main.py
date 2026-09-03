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
def dashboard():

    bugs = Bug.query.order_by(
        Bug.created_at.desc()
    ).all()

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

    print(
        "DASHBOARD TOTAL BUGS:",
        total_bugs
    )

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

        print(
            "CREATING BUG..."
        )

        print(
            "CURRENT USER ID:",
            current_user.id
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


            print(
                "BUG SAVED SUCCESSFULLY"
            )

            print(
                "BUG ID:",
                new_bug.id
            )

            print(
                "BUG USER ID:",
                new_bug.user_id
            )

            print(
                "TOTAL BUGS AFTER SAVE:",
                Bug.query.count()
            )


            flash(
                "Bug reported successfully!",
                "success"
            )


            return redirect(
                url_for(
                    "main.dashboard"
                )
            )


        except Exception as error:

            db.session.rollback()


            print(
                "ERROR SAVING BUG:",
                str(error)
            )


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