from flask import Flask, request, redirect, render_template, session
from flask_session import Session
from datetime import datetime, timedelta
from helpers import apology, login_required, showTimeOptions
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///meetUP.db")

# prevent caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    # Forget any userID
    session.clear()
    return render_template("index.html")


@app.route("/createEvent", methods=["GET", "POST"])
def createEvent():
    if request.method == "POST":

        # validate eventname
        if not request.form.get("eventName"):
            return apology("Please enter an event name", 400)

        # validate startdate
        elif not request.form.get("startDate"):
            return apology("Please choose a start date/time", 400)

        # validate enddate
        elif not request.form.get("endDate"):
            return apology("Please choose an end date/time", 400)

        else:
            # change dates into int
            startDate = datetime.strptime(request.form.get("startDate"), "%Y-%m-%dT%H:%M")
            endDate = datetime.strptime(request.form.get("endDate"), "%Y-%m-%dT%H:%M")

            # validate that startDate is before endDate
            if startDate >= endDate:
                return apology("Start date must be before end date", 400)

            eventName = request.form.get("eventName")
            eventHash = generate_password_hash(eventName, method='pbkdf2', salt_length=16)

            # create event in table[events]
            db.execute("INSERT INTO events(eventName, startDate, endDate, eventHash)VALUES(?, ?, ?, ?)", eventName, startDate, endDate, eventHash)

            # generate sharable link
            event_id = str(db.execute("SELECT eventID FROM events WHERE eventHash = ?", eventHash)[0]["eventID"])

            return redirect("/event/" + event_id)

    else:
        return render_template("createEvent.html")

###CHANGE EVENTLINK WHEN DEPLOYING WEBSITE####
@app.route("/event/<event_id>", methods=["GET", "POST"])
def event(event_id):
    eventID = event_id
    eventName = db.execute("SELECT eventName FROM events WHERE eventID = ?", eventID)[0]["eventName"]
    eventLink = "https://upgraded-xylophone-wwg5gj96gpw25rjp-5000.app.github.dev/event/" + str(eventID)

    return render_template("event.html", eventName=eventName, eventLink=eventLink, eventID=eventID)


@app.route("/register/<event_id>", methods=["GET", "POST"])
def register(event_id):
    eventID = event_id
    if request.method == "POST":
        userName = request.form.get("userName")
        password = request.form.get("password")

        # check for an userName
        if not userName:
            return apology("Please enter an user name", 400)

        # check if this username has already been used in the same event
        existedUser = db.execute("SELECT memberID FROM members WHERE memberName = ? AND eventID = ?", userName, eventID)
        if existedUser:
            return apology("This user name has already been used", 400)

        # check for a password
        elif not password:
            return apology("Please enter a password", 400)

        # record user info to table[members]
        else:
            passwordHash = generate_password_hash(password, method='pbkdf2', salt_length=16)
            db.execute("INSERT INTO members(memberName, eventID, passwordHash) VALUES(?, ?, ?)", userName, eventID, passwordHash)
            session["userID"] = db.execute("SELECT memberID FROM members WHERE memberName = ? AND eventID = ?", userName, eventID)[0]["memberID"]
            session["eventID"] = eventID
            return redirect("/schedule/" + eventID)

    else:
        return render_template("register.html", eventID=eventID)


@app.route("/logout/<eventID>")
def logout(eventID):

    # Forget any userID
    session.clear()

    # Redirect user to index page
    return redirect("/event/" + eventID)


@app.route("/login/<eventID>", methods=["GET", "POST"])
def login(eventID):
    if request.method == "POST":
        userName = request.form.get("userName")
        password = request.form.get("password")

        # check for an userName
        if not userName:
            return apology("Please enter an user name", 400)

        # check for a password
        elif not password:
            return apology("Please enter a password", 400)

        # check if account exists and password is correct
        rows = db.execute("SELECT * FROM members WHERE memberName = ? AND eventID = ?", userName, eventID)
        if len(rows) != 1 or not check_password_hash(rows[0]["passwordHash"], password):
            return apology("Invalid username and/or password", 400)

        # Remember which user has logged in
        else:
            session["userID"] = rows[0]["memberID"]
            return redirect("/result/" + eventID)
    else:
        return render_template("login.html", eventID=eventID)


@app.route("/schedule/<eventID>", methods=["GET", "POST"])
@login_required
def schedule(eventID):
    eventName = db.execute("SELECT eventName FROM events WHERE eventID = ?", eventID)[0]["eventName"]
    eventLink = "https://upgraded-xylophone-wwg5gj96gpw25rjp-5000.app.github.dev/event/" + str(eventID)

    if request.method == "POST":

        # record availabilty into table[availability]
        avaTime = request.form.getlist("avaTime")
        print(avaTime)

        for avatime in avaTime:
            db.execute("INSERT INTO availability(eventID, memberID, time) VALUES(?, ?, ?)", eventID, session["userID"], avatime)

        return redirect("/result/" + eventID)

    else:
        # SHOW TIME OPTIONS
        Time = showTimeOptions(db,eventID)

        return render_template("schedule.html", eventID=eventID, Time=Time, eventName=eventName, eventLink=eventLink)


@app.route("/result/<eventID>", methods=["GET"])
@login_required
def result(eventID):
    eventName = db.execute("SELECT eventName FROM events WHERE eventID = ?", eventID)[0]["eventName"]
    eventLink = "https://upgraded-xylophone-wwg5gj96gpw25rjp-5000.app.github.dev/event/" + str(eventID)

    # sort all available time
    allAva = db.execute("SELECT time, COUNT(memberID) as memberCount FROM availability WHERE eventID = ? GROUP BY time ORDER BY memberCount DESC", eventID)
    if not allAva:
        return apology("There isn't a best time, please reschedule", 403)
    else:
        # find top choice date&time
        top = allAva[0]["time"]

        # show avaMemb & notAvaMemb's ratio
        avaMemb = 0
        notAvaMemb = 0

        # show top date's members
        topMemb_dict = db.execute("SELECT memberName FROM members WHERE memberID IN (SELECT memberID FROM availability WHERE time = ?)", top)
        topMemb = []
        for i in range(len(topMemb_dict)):
            memb = topMemb_dict[i]["memberName"]
            topMemb.append(memb)
            avaMemb += 1

        # show top date's unavailable members
        topMemb_no_dict = db.execute("SELECT memberName FROM members WHERE eventID = ? AND memberID NOT IN (SELECT memberID FROM availability WHERE time = ?)", eventID, top)
        topMemb_no = []
        for i in range(len(topMemb_no_dict)):
            memb = topMemb_no_dict[i]["memberName"]
            topMemb_no.append(memb)
            notAvaMemb += 1

        # calculate allMemb
        topMembLen = len(topMemb)
        topNoLen = len(topMemb_no)
        allMemb = topMembLen + topNoLen


    return render_template("result.html", topMembLen=topMembLen, topNoLen=topNoLen, eventID=eventID, eventName=eventName, eventLink=eventLink, top=top, topMemb=topMemb, topMemb_no=topMemb_no, avaMemb=avaMemb, notAvaMemb=notAvaMemb, allMemb=allMemb)