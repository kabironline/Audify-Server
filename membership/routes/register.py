from flask import render_template, request, redirect, url_for
from membership.services import create_user, get_user_by_username


def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        nickname = request.form.get("nickname")
        bio = request.form.get("bio")

        # Checking for errors
        if get_user_by_username(username) is not None:
            return render_template(
                "membership/register.html",
                error="Username already taken, please choose another",
            )
        try:
            create_user(username, password, nickname, bio)
        except Exception as e:
            return render_template("membership/register.html", error=str(e))
        return redirect(url_for("login"))
    return render_template("membership/register.html")
