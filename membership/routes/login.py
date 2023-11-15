from flask import render_template, request, redirect, url_for
from membership.services import get_user_by_username
import core


def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username)
        print(password)

        if username is None or password is None:
            return render_template(
                "membership/login.html", error="Please fill all fields"
            )

        user = get_user_by_username(username)
        if user is None:
            return render_template("membership/login.html", error="User not found")
        elif user.password != password:
            return render_template(
                "membership/login.html", error="Password entered is incorrect"
            )

        core.set_current_user(user)
        return redirect(url_for("home"))
    return render_template("membership/login.html")


def logout():
    core.logout()
    return redirect(url_for("login"))
