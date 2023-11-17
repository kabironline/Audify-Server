from music.models import Genre, Track
from core.db import get_session


def create_genre(name, color):
    session = get_session()

    new_genre = Genre(
        name=name,
        color=color,
    )

    session.add(new_genre)
    session.commit()

    return new_genre


def get_genre_by_id(genre_id):
    session = get_session()

    genre = session.query(Genre).filter(Genre.id == genre_id).first()

    return genre


def get_genre_by_name(name):
    session = get_session()

    genre = session.query(Genre).filter(Genre.name == name).first()

    return genre


def get_all_genres():
    session = get_session()

    genres = session.query(Genre).all()

    return genres


def update_genre(genre_id, name, color):
    session = get_session()

    genre = session.query(Genre).filter(Genre.id == genre_id).first()

    genre.name = name if name is not None else genre.name
    genre.color = color if color is not None else genre.color

    session.commit()

    return genre


def delete_genre(genre_id):
    session = get_session()

    genre = session.query(Genre).filter(Genre.id == genre_id).first()

    session.delete(genre)
    session.commit()

    return True
