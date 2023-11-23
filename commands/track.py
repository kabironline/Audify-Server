import click
from flask.cli import with_appcontext
import music.services as music_services
from membership.services import channel as channel_services
import os


@click.command(name="update_genre_list")
@with_appcontext
def update_genre_list():
    # Open the file genre_list.csv
    # Loop through the lines
    # Get the genre (name), color
    # Create the genre if it doesn't exist

    f = open(
        os.path.join(os.path.dirname(__file__), "genre_list.csv"),
        "r",
        encoding="utf-8",
    )
    lines = f.readlines()
    f.close()

    for line in lines[1:]:
        genre_name, color = line.split(",")
        genre_name = genre_name.strip('"')
        color = color.strip('"').strip("\n")

        genre = music_services.get_genre_by_name(genre_name)

        if genre is not None:
            music_services.update_genre(genre_id=genre.id, color=color)
            continue

        music_services.create_genre(name=genre_name, color=color)


@click.command(name="get_track_list")
@with_appcontext
def get_track_list():
    # Create a file called track_list.csv
    # with the following columns:
    # track_id, track_name

    # Get all tracks
    tracks = music_services.get_all_tracks()

    # Open the file
    with open(
        os.path.join(os.path.dirname(__file__), "track_list.csv"), "w", encoding="utf-8"
    ) as track_list_file:
        # Writing the header
        track_list_file.write("track_id,track_name,creator_name\n")

        # Loop through the tracks
        for track in tracks:
            # Write the track_id and track_name
            creator_name = channel_services.get_channel_by_id(track.channel_id).name
            track_list_file.write(f'{track.id},"{track.name}", "{creator_name}"\n')


@click.command(name="update_track_from_list")
@with_appcontext
def update_track_from_list():
    # Open the file track_list_update.csv
    # Loop through the lines
    # Get the track_id, track_name, creator_name and genre_id from each line
    # Update the track with the track_id

    f = open(
        os.path.join(os.path.dirname(__file__), "track_list_updated.csv"),
        "r",
        encoding="utf-8",
    )
    lines = f.readlines()
    f.close()

    for line in lines[1:]:
        track_id, genre = line.split(",")
        track_id = int(track_id)
        genre = genre.strip('"').strip("\n")

        genre_id = music_services.get_genre_by_name(genre).id

        music_services.update_track(
            track_id=track_id,
            genre=genre_id,
        )


@click.command(name="generate_random_likes")
def generate_random_likes():
    user_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    import random

    for tracks in music_services.get_all_tracks():
        for user_id in user_ids:
            rating = random.random()
            if rating < 0.6:
                rating = 1
            else:
                rating = 0
            music_services.create_or_update_rating(
                user_id=user_id,
                track_id=tracks.id,
                rating=rating,
            )


@click.command(name="generate_random_views")
def generate_random_views():
    user_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    import random

    for track in music_services.get_all_tracks():
        for user_id in user_ids:
            view = random.random()
            if view < 0.6:
                music_services.create_new_view(
                    track=track[0],
                    user_id=user_id,
                )
