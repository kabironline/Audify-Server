from flask import Flask, redirect, url_for, request, Response, render_template
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import core

from core.utils import *
from commands.db import *
from commands.track import *
from core.db import db
from core import api
from membership.models import User
import membership.routes
import membership.api_old
import membership.api
import music.routes
import music.api_old
import music.api
import music.models
import admin.routes

app = Flask(__name__)
app.secret_key = "secret_key"
CORS(app, resources={r"/*": {"origins": "*"}})

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "core/db/db.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = False

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "6d7f095ee80911f504e7bafaef6ad6169a15870146c604dbb11b7fa7f98809ac"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

api = Api(app)

api.add_resource(
    music.api_old.RatingAPI,
    "/api/v1/rating/<int:track_id>",
)
api.add_resource(
    music.api_old.CommentAPI,
    "/api/v1/comment/<int:track_id>",
    "/api/v1/comment/<int:track_id>/<int:comment_id>",
)

api.add_resource(
    music.api_old.TrackAPI,
    "/api/v1/track",
    "/api/v1/track/<int:track_id>",
)

api.add_resource(
    membership.api_old.UserAPI,
    "/api-old/v1/user",
    "/api-old/v1/user/<int:user_id>",
    "/api-old/v1/user/<string:username>",
)

api.add_resource(
    membership.api_old.ChannelAPI,
    "/api-old/v1/channel",
    "/api-old/v1/channel/<int:channel_id>",
    "/api-old/v1/channel/<string:channel_name>",
)

# V2 API

api.add_resource(
    membership.api.LoginAPI,
    "/api/v2/login",
)

api.add_resource(
    membership.api.UserAPIV2,
    "/api/v2/user",
    "/api/v2/user/<int:user_id>",
    "/api/v2/user/<string:username>",
)

api.add_resource(
    music.api.RecentsAPI,
    "/api/v2/tracks/recents"
)

api.add_resource(
    music.api.LatestAPI,
    "/api/v2/tracks/latest",
    "/api/v2/albums/latest",
    "/api/v2/playlists/latest",
)

core.set_api(api)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers["X-Content-Type-Options"] = "*"
        return res


# Devop commands
# app.cli.add_command(create_tables)
# app.cli.add_command(drop_table)
# app.cli.add_command(drop_all_tables)
# app.cli.add_command(create_superuser)
# app.cli.add_command(get_track_list)
# app.cli.add_command(update_track_from_list)
# app.cli.add_command(update_genre_list)
# app.cli.add_command(generate_random_likes)
# app.cli.add_command(generate_random_views)
# app.cli.add_command(update_channelname)
# app.cli.add_command(update_track_duration)

app.cli.add_command(create_superuser)
app.cli.add_command(get_track_list)
app.cli.add_command(generate_random_likes)
app.cli.add_command(generate_random_views)
app.cli.add_command(update_track_duration)

# @jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

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

app.add_url_rule(
    "/user/<int:user_id>/delete",
    "user_delete",
    membership.routes.delete_user,
    methods=["POST"],
)

app.add_url_rule(
    "/channel/<int:channel_id>/delete",
    "channel_delete",
    membership.routes.delete_channel,
    methods=["POST"],
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

app.add_url_rule("/track/flag", "track_flag", music.routes.track_flag, methods=["POST"])
app.add_url_rule(
    "/track/unflag/<int:track_id>",
    "track_unflag",
    music.routes.track_unflag,
)

app.add_url_rule(
    "/tracks/<int:track_id>/edit",
    "track_edit",
    music.routes.track_edit,
    methods=["GET", "POST"],
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
app.add_url_rule(
    "/top_charts/tracks/views", "top_tracks_view", music.routes.top_charts_tracks
)
app.add_url_rule(
    "/top_charts/tracks/rating", "top_tracks_rating", music.routes.top_rated_tracks
)
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
    "/dashboard/channel/<int:channel_id>/tracks/list",
    "dashboard_channel_tracks_list",
    membership.routes.dashboard_channel_track_list,
)

app.add_url_rule(
    "/rating/<int:track_id>/<int:rating>",
    "update_rating",
    music.routes.update_rating,
)

app.add_url_rule(
    "/channels/<int:channel_id>/whitelist",
    "whitelist_channel",
    admin.routes.whitelist_channel,
)

app.add_url_rule(
    "/channels/<int:channel_id>/blacklist",
    "blacklist_channel",
    admin.routes.blacklist_channel,
)

app.add_url_rule(
    "/edit_profile",
    "edit_profile",
    membership.routes.edit_profile,
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/edit_profile_creator",
    "edit_profile_creator",
    membership.routes.edit_profile_creator,
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

app.add_url_rule(
    "/album/<int:album_id>/cover",
    "album_cover_new",
    music.routes.album_cover,
)
app.add_url_rule(
    "/admin/dashboard",
    "admin_dashboard",
    admin.routes.admin_dashboard,
)

app.add_url_rule(
    "/admin/dashboard/blacklist",
    "admin_dashboard_blacklist",
    admin.routes.admin_dashboard_blacklist,
)

app.add_url_rule(
    "/admin/dashboard/whitelist",
    "admin_dashboard_whitelist",
    admin.routes.admin_dashboard_whitelist,
)

app.add_url_rule(
    "/admin/dashboard/tracks",
    "admin_dashboard_tracks",
    admin.routes.admin_dashboard_tracks,
)


@app.errorhandler(404)
def page_not_found(e=None):
    return render_template("404.html"), 404


app.add_url_rule(
    "/404",
    "page_not_found",
    page_not_found,
)


@app.context_processor
def inject_user():
    return dict(current_user=core.get_current_user())


app.jinja_env.filters["format_duration"] = format_duration
app.jinja_env.filters["format_duration_words"] = format_duration_words
app.jinja_env.filters["playlist_total_duration"] = playlist_total_duration
app.jinja_env.filters[
    "format_datetime_for_html_default"
] = format_datetime_for_html_default

app.add_url_rule(
    "/media/<path:filename>",
    "media",
    build_only=True,
    subdomain="static",
)

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 5000, app, use_reloader=True, use_debugger=True)
