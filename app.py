from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMENANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def usd(value):
    return f"${value:,.2f}"

db = SQL("sqlite:///casino.db")
# CREATE UNIQUE INDEX username ON users (username); creates an index called username for the username column in users which makes its retrieval faster

bet_choices = []
for i in range(100, 1001, 100):
    bet_choices.append(i)


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
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        dollars = request.form.get('dollars')
        cents = request.form.get('cents')
        total = int(dollars) + int(cents) / 100

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        return render_template('profile.html', cash=usd(cash[0]['cash']))


@app.route("/poker-betting", methods=["GET", "POST"])
def pokerBetting():
    global bet
    if request.method == "GET":
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        bet = request.args.get("dollars")
        if int(bet) > int(cash[0]["cash"]):
            return render_template("pokerBettingFailure.html", cash=usd(cash[0]['cash']), choices=bet_choices)
        else:
            return render_template("poker.html")
    else:
        if request.form['again'] == 'Dealer wins':
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", 2 * int(bet), session["user_id"])
        elif request.form['again'] == 'Dealer wins by fold':
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", bet, session["user_id"])
        elif request.form['again'] == 'Player wins':
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", 2 * int(bet), session["user_id"])
        return render_template('poker_betting.html', cash=usd(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]), choices=bet_choices)

@app.route("/blackjack-betting", methods=["GET", "POST"])
def blackjackBetting():
    global bett
    if request.method == "GET":
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        bett = request.args.get("dollars")
        if int(bett) > int(cash[0]["cash"]):
            return render_template("blackjackBettingFailure.html", cash=usd(cash[0]['cash']), choices=bet_choices)
        else:
            return render_template("blackjack.html")
    else:
        if 'Win' in request.form['again']:
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", int(bett), session["user_id"])
        elif 'Lose' or 'Bust' in request.form['again']:
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", int(bett), session["user_id"])
        else:
            pass
        return render_template('blackjack_betting.html', cash=usd(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]), choices=bet_choices)

@app.route("/blackjack")
def blackjack():
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    return render_template("blackjack_betting.html", cash=usd(cash[0]['cash']), choices=bet_choices)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("invalid_login.html")

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

@app.route("/poker")
def poker():
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    return render_template("poker_betting.html", cash=usd(cash[0]['cash']), choices=bet_choices)


@app.route("/profile")
def profile():
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    return render_template("profile.html", cash=usd(cash[0]['cash']))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    else:
        if len(db.execute("SELECT * FROM users WHERE username = ?" , request.form.get("username")))!= 0:
            return render_template("register_error.html")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
            return redirect("/login")


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == 'GET':
        return render_template("reset.html")
    else:
        new = request.form.get('new')
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new), session["user_id"])
        return render_template('profile.html', cash=usd(cash[0]['cash']))