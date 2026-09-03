from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user
)

from models import db
from models.user import User


auth = Blueprint(
    "auth",
    __name__
)


@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )


    if request.method == "POST":

        username = request.form.get(
            "username"
        ).strip()

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )


        existing_username = User.query.filter_by(
            username=username
        ).first()


        existing_email = User.query.filter_by(
            email=email
        ).first()


        if existing_username:

            flash(
                "Username already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        if existing_email:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )


        new_user = User(
            username=username,
            email=email
        )

        new_user.set_password(
            password
        )


        db.session.add(new_user)

        db.session.commit()


        login_user(new_user)


        flash(
            "Account created successfully!",
            "success"
        )


        return redirect(
            url_for("main.dashboard")
        )


    return render_template(
        "register.html"
    )


@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )


        user = User.query.filter_by(
            email=email
        ).first()


        if user and user.check_password(password):

            login_user(user)


            flash(
                "Welcome back!",
                "success"
            )


            return redirect(
                url_for("main.dashboard")
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "login.html"
    )


@auth.route("/logout")
def logout():

    logout_user()


    flash(
        "You have been logged out.",
        "info"
    )


    return redirect(
        url_for("main.home")
    )