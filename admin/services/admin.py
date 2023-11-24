import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from music.services import (
    get_all_tracks,
    get_all_genres,
    get_all_albums,
    get_all_playlists,
    get_genre_tracks,
)
import os
from membership.services import get_all_channels, get_all_users
from flask import send_file


def generate_genre_distribution_graph():
    # Generate a pie chart of the genre distribution

    genre = get_all_genres()

    genre_names = []
    genre_counts = []
    for g in genre:
        genre_names.append(g.name)
        genre_counts.append(len(get_genre_tracks(g.id)))

    # Clear the plot from previous runs
    plt.clf()

    plt.pie(genre_counts, labels=genre_names, autopct="%1.1f%%")
    plt.axis("equal")
    plt.title("Genre Distribution")
    # make the background black and the color of the pies the color of the genre
    plt.style.use("dark_background")
    # Add a legend
    plt.legend(title="Genres", loc="upper right")
    plt.savefig("static/images/genre_distribution.png")

    return send_file("static/images/genre_distribution.png", mimetype="image/png")


def generate_user_channel_distribution_graph():
    # Generate a pie chart of the ratio between total users / total channels

    users = get_all_users()
    channels = get_all_channels()

    plt.clf()

    plt.pie(
        [len(users), len(channels)], labels=["Users", "Channels"], autopct="%1.1f%%"
    )
    plt.axis("equal")
    plt.title("User / Channel Distribution")
    # make the background black and the color of the pies the color of the genre
    plt.style.use("dark_background")
    # Add a legend
    plt.legend(title="Users / Channels", loc="upper right")
    plt.savefig("static/images/user_channel_distribution.png")

    return send_file(
        "static/images/user_channel_distribution.png", mimetype="image/png"
    )

