from flask import render_template, request, redirect, url_for
from membership.services import get_user_by_id
import core


def dashboard(user_id=None):
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    if user_id is None or user_id == core.get_current_user().id:
        return render_template(
            "membership/dashboard.html", user=core.get_current_user(), self=False
        )
    else:
        user = get_user_by_id(user_id)
        
        return render_template("membership/dashboard.html", user=user, self=True)
