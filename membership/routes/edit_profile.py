from flask import render_template, request, redirect, url_for
import core
from membership.services import update_user


def edit_profile():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        request_data = request.form
        if request_data.get("password") != user.password:
            return render_template(
                "membership/edit_profile.html",
                current_user=user,
                error="Incorrect Old Password Password",
            )

        user.username = request_data.get("username")
        user.nickname = request_data.get("nickname")
        user.bio = request_data.get("bio")

        if request_data.get("new_password") != "":
            user.password = request_data.get("new_password")

        request_data = request.files
        user.avatar = None
        if request_data.get("avatar"):
            user.avatar = request_data.get("avatar")

        update_user(user)
        return redirect(url_for("edit_profile"))

    return render_template("membership/edit_profile.html", current_user=user)
