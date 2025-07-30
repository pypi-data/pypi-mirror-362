import datetime


def get_date_time_to_utc_server_time_format_string(date_time_inst: datetime.datetime) -> str:
    """
    Convert a datetime object to UTC format string: YYYY-MM-DDTHH:MM:SS.fffffZ

    Args:
        dt: datetime object (can be naive or timezone-aware)

    Returns:
        str: UTC formatted string ending with 'Z'
    """
    # If datetime is naive (no timezone info), assume it's UTC
    if date_time_inst.tzinfo is None:
        dt = date_time_inst.replace(tzinfo=datetime.timezone.utc)

    # Convert to UTC if it's in a different timezone
    dt_utc = date_time_inst.astimezone(datetime.timezone.utc)

    # Format to ISO string with microseconds and 'Z' suffix
    return dt_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')