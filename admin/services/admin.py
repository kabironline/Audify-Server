import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from music.services import (
    get_all_tracks,
    get_all_genres,
    get_genre_tracks,
)
from music.services.view import get_views_by_genre_id, get_views_by_date
from membership.services import get_all_channels, get_all_users
from flask import send_file
import plotly.express as px
from datetime import datetime, timedelta


def generate_genre_distribution_graph(data_only=False):
    genre = get_all_genres()

    genre_names = []
    genre_counts = []
    for g in genre:
        genre_names.append(g.name)
        genre_counts.append(len(get_genre_tracks(g.id)))

    if data_only:
        return {
            "labels": genre_names,
            "values": genre_counts,
            "type": "pie",
            "backgroundColor": "rgba(0,0,0,0)",
        }


    fig = px.pie(
        values=genre_counts,
        names=genre_names,
        title="Genre Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu,
    )

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_font_size=30, title_x=0.5, title_font_color="white")
    fig.update_layout(legend_bgcolor="white")
    return fig.to_html(full_html=False)


def generate_user_channel_distribution_graph(data_only=False):
    users = get_all_users()
    channels = get_all_channels()

    if data_only:
        return {
            "labels": ["Users", "Channels"],
            "values": [len(users), len(channels)],
            "type": "pie",
            "backgroundColor": "rgba(0,0,0,0)",
        }

    fig = px.pie(
        values=[len(users), len(channels)],
        names=["Users", "Channels"],
        title="User/Channel Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu,
    )

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_font_size=30, title_x=0.5, title_font_color="white")
    fig.update_layout(legend_bgcolor="white")

    return fig.to_html(full_html=False)


def generate_genre_listener_graph(data_only=False):
    genre = get_all_genres()

    genre_names = []
    genre_counts = []
    for g in genre:
        genre_names.append(g.name)
        genre_views = get_views_by_genre_id(g.id)
        genre_counts.append(genre_views)

    if data_only:
        return {
            "x": genre_names,
            "y": genre_counts,
            "type": "bar",
            "backgroundColor": "rgba(0,0,0,0)",
            "sort": "total descending",
        }

    fig = px.bar(
        x=genre_names,
        y=genre_counts,
        title="Genre Listeners",
        color_discrete_sequence=px.colors.sequential.RdBu,
    )

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(title_font_size=30, title_x=0.5, title_font_color="white")
    fig.update_layout(legend_bgcolor="white")
    fig.update_xaxes(categoryorder="total descending", title_text="Genre")
    fig.update_yaxes(title_text="Listeners")
    fig.update_traces(marker_color="white")
    fig.update_xaxes(tickfont_color="white")
    fig.update_yaxes(tickfont_color="white")
    fig.update_xaxes(title_font_color="white")
    fig.update_yaxes(title_font_color="white")

    return fig.to_html(full_html=False)


def generate_recent_viewership_graph(data_only=False):
    # Gets the last 7 days of views

    today = datetime.now()
    dates = [today - timedelta(days=i) for i in range(7)]
    dates.reverse()
    views = [get_views_by_date(date) for date in dates]

    if data_only:
        return {
            "x": [str(date.date()) for date in dates],
            "y": views,
            "type": "line",
            "backgroundColor": "rgba(0,0,0,0)",
        }

    fig = px.line(
        x=dates,
        y=views,
        title="Recent Listenership",
        color_discrete_sequence=px.colors.sequential.RdBu,
    )

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(title_font_size=30, title_x=0.5, title_font_color="white")
    fig.update_layout(legend_bgcolor="white")
    fig.update_xaxes(categoryorder="total descending", title_text="Dates")
    fig.update_yaxes(title_text="Total Listenership")
    fig.update_traces(marker_color="white")
    fig.update_xaxes(tickfont_color="white")
    fig.update_yaxes(tickfont_color="white")
    fig.update_xaxes(title_font_color="white")
    fig.update_yaxes(title_font_color="white")
    fig.update_traces(line=dict(color="yellow", width=4))

    return fig.to_html(full_html=False)
