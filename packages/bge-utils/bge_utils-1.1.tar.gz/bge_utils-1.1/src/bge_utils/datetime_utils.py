import time


def time_since(past_timestamp):
    """
    =============================
    Time Since Utility
    =============================

    This function calculates the time elapsed since a given past timestamp.

    :param past_timestamp: The past timestamp to calculate the time since.
    :type past_timestamp: float

    :returns: A string representing the time elapsed in a human-readable format:

        - **seconds** → If the elapsed time is less than 60 seconds
        - **minutes** → If the elapsed time is less than 60 minutes
        - **hours** → If the elapsed time is less than 24 hours
        - **days** → If the elapsed time is 24 hours or more
    :rtype: str

    **Example Usage**
    -----------------
    .. code-block:: python

        past_time = time.time() - 3600  # 1 hour ago
        result = time_since(past_time)
        print(result)  # '1 hours ago'

    **See Also**
    ------------
    - `time <https://docs.python.org/3/library/time.html>`_
    """
    now = time.time()
    diff = now - past_timestamp
    if diff < 60:
        return f"{int(diff)} seconds ago"
    elif diff < 3600:
        minutes = int(diff / 60)
        return f"{minutes} minutes ago"
    elif diff < 86400:
        hours = int(diff / 3600)
        return f"{hours} hours ago"
    else:
        days = int(diff / 86400)
        return f"{days} days ago"


def find_timezone_difference(timezone2):
    """
    =============================
    Timezone Difference Utility
    =============================

    This function calculates the time difference between Amsterdam and another timezone.

    :param timezone2: The second timezone.
    :type timezone2: str

    :returns: A string representing the time difference between the two timezones.
    :rtype: str

    **Example Usage**
    -----------------
    .. code-block:: python

        result = find_timezone_difference('America/New_York')
        print(result)  # 'The given timezone is 5 hours and 0 minutes behind Amsterdam.'

    **See Also**
    ------------
    - `pytz <https://pypi.org/project/pytz/>`_
    - `Supported Timezones <https://www.php.net/manual/en/timezones.php>`_
    """
    from datetime import datetime
    from pytz import timezone

    tz1 = timezone("Europe/Amsterdam")
    tz2 = timezone(timezone2)

    time1 = datetime.now(tz1)
    time2 = datetime.now(tz2)

    time1 = time1.utcoffset()
    time2 = time2.utcoffset()

    # Calculate the time difference
    time_difference = time2 - time1  # type: ignore

    # Convert the time difference to hours and minutes
    hours_offset = time_difference.total_seconds() // 3600
    minutes_offset = (time_difference.total_seconds() % 3600) // 60

    # Determine if timezone2 is ahead or behind timezone1
    if hours_offset > 0 or (hours_offset == 0 and minutes_offset > 0):
        return f"The given timezone is {int(hours_offset)} hours and {int(minutes_offset)} minutes ahead of Amsterdam."
    elif hours_offset < 0 or (hours_offset == 0 and minutes_offset < 0):
        return f"The given timezone is {int(abs(hours_offset))} hours and {int(abs(minutes_offset))} minutes behind Amsterdam."
    else:
        return "The given timezone is the same as Amsterdam."
