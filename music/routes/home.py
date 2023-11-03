from flask import render_template, request, redirect, url_for
from membership.services import get_user_by_username
import core


def home():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return render_template("music/home.html")
