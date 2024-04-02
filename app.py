import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # distinct stocks
    temp = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id = ?", session["user_id"])
    distinct_stocks = []
    for t in temp:
        distinct_stocks.append(t["symbol"])

    # for each symbol, create a dict for detail info, including symbol, shares, current price, total value
    stock_total_value = 0
    index = {}
    for stock in distinct_stocks:
        stock_info = {}
        stock_info["symbol"] = stock
        stock_info["shares"] = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user_id = ?", stock, session["user_id"])[0]["SUM(shares)"]
        stock_info["cur_price"] = lookup(stock)["price"]
        stock_info["total_value"] = stock_info["shares"] * stock_info["cur_price"]

        stock_total_value += stock_info["total_value"]

        index[stock_info["symbol"]] = stock_info

    # cash balance & grand total
    cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    grand_total = cash + stock_total_value

    return render_template("index.html", distinct_stocks=distinct_stocks, index=index, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stockInfo = lookup(symbol)

        # check symbol
        if not symbol:
            return apology("Please enter a symbol", 400)
        elif not stockInfo:
            return apology("This symbol does not exist", 400)

        # check shares
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Please enter a positive integer", 400)

        if not shares:
            return apology("Please enter how many shares to buy", 400)
        elif shares <= 0:
            return apology("Please enter a positive integer", 400)

        # buy stock
        price = float(stockInfo["price"])
        totalPrice = price * shares
        userCash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
        if totalPrice > userCash:
            return apology("Sorry, your balance is not enough to fulfill the purchase", 400)
        else:
            flash("Successfully purchased stock!")
            userBalance = userCash - totalPrice
            db.execute("UPDATE users SET cash = ? WHERE id = ?", userBalance, session["user_id"])

            # record transaction to database
            usernameList = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
            username = usernameList[0]["username"]
            db.execute("INSERT INTO transactions(user_id, username, symbol, totalPrice, time, shares, type) VALUES(?, ?, ?, ?, datetime('now'), ?, 'buy')",
                       session["user_id"], username, symbol, totalPrice, shares)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, type, totalPrice, shares, time FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote_result = lookup(symbol)

        if quote_result:
            return render_template("quoted.html", quote_result=quote_result)
        else:
            return apology("This symbol does not exist", 400)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # check username
        username = request.form.get("username")
        exist_usernames = db.execute("SELECT username FROM users WHERE username=?", username)
        if not username:
            return apology("Please enter a username", 400)
        if exist_usernames:
            return apology("This username already has an account", 400)

        # check password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology("Please enter a password", 400)
        if not confirmation:
            return apology("Please enter a confirmation password", 400)
        if confirmation != password:
            return apology("Confirmation password does not match password", 400)

        # insert user registeration into database
        hashed_password = generate_password_hash(password, method='pbkdf2', salt_length=16)
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hashed_password)

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # distinct stocks
    temp = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id = ?", session["user_id"])
    distinct_stocks = []
    for t in temp:
        distinct_stocks.append(t["symbol"])

    if request.method == "POST":

        selected_stock = request.form.get("symbol")
        selected_stock_shares = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user_id = ?", selected_stock, session["user_id"])[0]["SUM(shares)"]

        # if fails to select stock
        if not selected_stock:
            return apology("Please select a stock symbol", 400)

        # if doesn't own the selected stock
        if selected_stock not in distinct_stocks:
            return apology("Sorry, you do not own any of this stock", 400)

        # if share input not positive int
        try:
            share_input = int(request.form.get("shares"))
        except ValueError:
            return apology("Please enter a positive integer for shares", 400)

        if share_input <= 0:
            return apology("Please enter a positive integer for shares", 400)

        # if user doesn't own that many shares
        if selected_stock_shares < share_input:
            return apology("You don't have that many shares", 400)

        # sell stock
        flash("Successfully sold stock!")
        price = float(lookup(selected_stock)["price"])
        totalPrice = float(price * share_input)
        userCash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
        userBalance = userCash + totalPrice
        db.execute("UPDATE users SET cash = ? WHERE id = ?", userBalance, session["user_id"])

        # record transaction to database
        usernameList = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = usernameList[0]["username"]
        db.execute("INSERT INTO transactions(user_id, username, symbol, totalPrice, time, shares, type) VALUES(?, ?, ?, ?, datetime('now'), ?, 'sell')",
                    session["user_id"], username, selected_stock, totalPrice, -share_input)

        return redirect("/")
    else:
        return render_template("sell.html", distinct_stocks=distinct_stocks)

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """change user password"""

    if request.method == "POST":
        old = request.form.get("old")
        new = request.form.get("new")
        hashed_new = generate_password_hash(new, method='pbkdf2', salt_length=16)
        correct = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]["hash"]

        if check_password_hash(correct, old) == False:
            return apology("Wrong Password", 400)
        else:
            flash("Password successfully changed")
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new, session["user_id"])

        return redirect("/")
    else:
        return render_template("password.html")
