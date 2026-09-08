from datetime import datetime


def get_current_datetime() -> str:
    """
    Return the current local date and time.

    Returns:
        The current date and time in ISO 8601 format.
    """

    return datetime.now().astimezone().isoformat()