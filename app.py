from commands.db import *
from core.db import db
from flask import Flask, redirect, url_for
import membership.routes
import music.routes
import os
import sys
import core


app = Flask(__name__)


current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
db_path = os.path.join(current_dir, "core/db/db.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

app.cli.add_command(create_tables)
app.cli.add_command(drop_table)
app.cli.add_command(drop_all_tables)
app.cli.add_command(create_superuser)


@app.route("/")
def entry():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return redirect(url_for("home"))


# @app.route('/login')
# def index():
#     return render_template('membership/login.html')

app.add_url_rule("/home", "home", music.routes.home)
app.add_url_rule("/login", "login", membership.routes.login, methods=["GET", "POST"])
app.add_url_rule(
    "/register", "register", membership.routes.register, methods=["GET", "POST"]
)
app.add_url_rule("/player", "player", music.routes.player)
app.add_url_rule("/explore", "explore", music.routes.explore)
app.add_url_rule("/new_releases", "new_releases", music.routes.new_releases)
app.add_url_rule(
    "/new_releases/albums", "new_releases_albums", music.routes.new_releases_albums
)
app.add_url_rule(
    "/new_releases/tracks", "new_releases_tracks", music.routes.new_releases_tracks
)
app.add_url_rule("/dashboard", "dashboard", membership.routes.dashboard)
app.add_url_rule("/dashboard/<int:user_id>", "dashboard", membership.routes.dashboard)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
