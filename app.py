from flask import Flask, redirect, url_for, request, Response, session
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
import os
import core

from commands.db import *
from commands.track import *
from core.db import db
from core import api
import membership.routes
import membership.api
import music.routes
import music.api
import music.models


app = Flask(__name__)
app.secret_key = "secret_key"
CORS(app, resources={r"/*": {"origins": "*"}})

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "core/db/db.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
api.add_resource(
    music.api.RatingAPI,
    "/api/v1/rating/<int:track_id>",
)
api.add_resource(
    music.api.CommentAPI,
    "/api/v1/comment/<int:track_id>",
    "/api/v1/comment/<int:track_id>/<int:comment_id>",
)

api.add_resource(
    music.api.TrackAPI,
    "/api/v1/track",
    "/api/v1/track/<int:track_id>",
)

api.add_resource(
    membership.api.UserAPI,
    "/api/v1/user",
    "/api/v1/user/<int:user_id>",
    "/api/v1/user/<string:username>",
)

api.add_resource(
    membership.api.ChannelAPI,
    "/api/v1/channel",
    "/api/v1/channel/<int:channel_id>",
    "/api/v1/channel/<string:channel_name>",
)

core.set_api(api)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers["X-Content-Type-Options"] = "*"
        return res


app.cli.add_command(create_tables)
app.cli.add_command(drop_table)
app.cli.add_command(drop_all_tables)
app.cli.add_command(create_superuser)
app.cli.add_command(get_track_list)
app.cli.add_command(update_track_from_list)
app.cli.add_command(update_genre_list)
app.cli.add_command(generate_random_likes)
app.cli.add_command(update_channelname)


@app.route("/")
def entry():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return redirect(url_for("home"))


app.add_url_rule("/home", "home", music.routes.home)
app.add_url_rule("/login", "login", membership.routes.login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", membership.routes.logout)

app.add_url_rule(
    "/register", "register", membership.routes.register, methods=["GET", "POST"]
)
app.add_url_rule(
    "/register_creator",
    "register_creator",
    membership.routes.register_creator,
    methods=["GET", "POST"],
)

app.add_url_rule("/search", "search", music.routes.search)

app.add_url_rule("/upload", "upload", music.routes.upload, methods=["GET", "POST"])
app.add_url_rule("/playlist", "playlist", music.routes.playlist_page, methods=["POST"])
app.add_url_rule(
    "/playlist/<int:playlist_id>",
    "playlist_page",
    music.routes.playlist_page,
    methods=["GET"],
)

app.add_url_rule(
    "/playlist/<int:playlist_id>/delete",
    "playlist_delete",
    music.routes.playlist_delete,
)

app.add_url_rule(
    "/playlist/<int:playlist_id>/update",
    "playlist_update",
    music.routes.playlist_update,
    methods=["POST"],
)
app.add_url_rule(
    "/playlist/add",
    "playlist_add",
    music.routes.playlist_add,
    methods=["POST"],
)

app.add_url_rule(
    "/playlist/<int:playlist_id>/delete/<int:track_id>",
    "playlist_track_delete",
    music.routes.playlist_track_delete,
)

app.add_url_rule(
    "/album/<int:album_id>",
    "album_page",
    music.routes.album_page,
)

app.add_url_rule(
    "/album/add",
    "album_add",
    music.routes.create_album_route,
    methods=["GET", "POST"],
)

app.add_url_rule(
    "/album/<int:album_id>/edit",
    "album_edit",
    music.routes.album_update_route,
    methods=["GET", "POST"],
)

app.add_url_rule(
    "/album/<int:album_id>/delete",
    "album_delete",
    music.routes.album_delete_route,
    methods=["GET", "POST"],
)


# Players and Tracks
app.add_url_rule("/player/<int:track_id>", "player", music.routes.player)
app.add_url_rule(
    "/player/album/<int:album_id>",
    "album_player",
    music.routes.player_list,
)
app.add_url_rule(
    "/player/album/<int:album_id>/<int:position>",
    "album_player_pos",
    music.routes.player_list,
)
app.add_url_rule(
    "/player/playlist/<int:playlist_id>",
    "playlist_player",
    music.routes.player_list,
)
app.add_url_rule(
    "/player/playlist/<int:playlist_id>/<int:position>",
    "playlist_player_pos",
    music.routes.player_list,
)
app.add_url_rule("/tracks/<int:track_id>", "track", music.routes.track)
app.add_url_rule(
    "/tracks/<int:track_id>/cover", "track_cover", music.routes.track_cover
)
app.add_url_rule(
    "/tracks/<int:track_id>/media", "track_media", music.routes.track_media
)
app.add_url_rule(
    "/track/delete", "track_delete", music.routes.track_delete, methods=["POST"]
)

# Comments
app.add_url_rule(
    "/tracks/<int:track_id>/comments",
    "create_comment",
    music.routes.post_comment_route,
    methods=["POST"],
)
app.add_url_rule(
    "/tracks/<int:track_id>/comments/<int:comment_id>/delete",
    "delete_comment",
    music.routes.delete_comment_route,
    # methods=["POST"],
)


app.add_url_rule("/player_controls", "player_controls", music.routes.player_controls)
app.add_url_rule("/explore", "explore", music.routes.explore)
app.add_url_rule("/new_releases", "new_releases", music.routes.new_releases)
app.add_url_rule(
    "/new_releases/albums", "new_releases_albums", music.routes.new_releases_albums
)
app.add_url_rule(
    "/new_releases/tracks", "new_releases_tracks", music.routes.new_releases_tracks
)
app.add_url_rule("/top_charts", "top_charts", music.routes.top_charts)
app.add_url_rule("/top_charts/tracks", "top_tracks", music.routes.top_charts_tracks)
app.add_url_rule("/dashboard", "dashboard", membership.routes.dashboard)
app.add_url_rule("/dashboard/<int:user_id>", "dashboard", membership.routes.dashboard)
app.add_url_rule(
    "/dashboard/channel/<int:channel_id>",
    "dashboard_channel",
    membership.routes.dashboard_channel,
)
app.add_url_rule(
    "/dashboard/channel/<int:channel_id>/tracks",
    "dashboard_channel_tracks",
    membership.routes.dashboard_channel_tracks,
)
app.add_url_rule(
    "/rating/<int:track_id>/<int:rating>",
    "update_rating",
    music.routes.update_rating,
)

app.add_url_rule(
    "/edit_profile",
    "edit_profile",
    membership.routes.edit_profile,
    methods=["GET", "POST"],
)

app.add_url_rule(
    "/genre/<int:genre_id>/tracks", "genre_tracks", music.routes.genre_tracks
)
app.add_url_rule(
    "/user_avatar/<int:user_id>", "user_avatar", membership.routes.user_avatar
)

app.add_url_rule(
    "/channel_avatar/<int:channel_id>",
    "channel_avatar",
    membership.routes.channel_avatar,
)

app.add_url_rule(
    "/album/cover/<int:album_id>",
    "album_cover",
    music.routes.album_cover,
)


@app.context_processor
def inject_user():
    return dict(current_user=core.get_current_user())


app.add_url_rule(
    "/media/<path:filename>",
    "media",
    build_only=True,
    subdomain="static",
)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
