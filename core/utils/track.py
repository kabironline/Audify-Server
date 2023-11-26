def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def format_duration_words(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours} hours and {minutes} minutes"
    else:
        return f"{minutes} minutes"


def playlist_total_duration(tracks: list):
    total_duration = 0
    for track in tracks:
        total_duration += track.duration

    return format_duration_words(total_duration)


def format_datetime_for_html_default(dt):
    """
    Function to format a datetime object to a string compatible with HTML datetime-local input.
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%S")
