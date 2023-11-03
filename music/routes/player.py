from flask import render_template, redirect, url_for
import core


def player():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return render_template("music/player.html")
