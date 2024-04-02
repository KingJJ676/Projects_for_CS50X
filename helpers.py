from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime, timedelta
from cs50 import SQL


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userID") is None:
            session["eventID"] = kwargs.get("eventID")
            return redirect("/register/<event_id>")
        return f(*args, **kwargs)

    return decorated_function


def showTimeOptions(db, eventID):

    # get event's time range & formating time into datetime objects
    temp = db.execute("SELECT startDate, endDate FROM events WHERE eventID = ?", eventID)[0]
    startTime = datetime.strptime(temp["startDate"], '%Y-%m-%d %H:%M:%S')
    endTime = datetime.strptime(temp["endDate"], '%Y-%m-%d %H:%M:%S')

    # insert time into list
    step_hour = timedelta(hours = 1)
    step_day = timedelta(days = 1)
    Time = {}

    while startTime <= endTime:
        date = startTime.date()
        next_day = startTime + step_day
        hours = []

        while startTime < next_day and startTime <= endTime:
            hours.append(startTime)
            startTime += step_hour

        # converting datetime.datetime to str.str
        date = datetime.strftime(date, '%Y-%m-%d')
        hours = [hour.strftime('%H:%M:%S') for hour in hours]
        Time[date] = hours

    return Time