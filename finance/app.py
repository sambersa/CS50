import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# utils.py


def usd(value):
    """Format value as USD."""
    try:
        # Convert value to float
        value = float(value)
    except (ValueError, TypeError):
        return "$0.00"  # Return a default value if conversion fails

    return f"${value:,.2f}"  # Format as USD


# Register the usd function for use in Jinja templates
app.jinja_env.globals.update(usd=usd)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.context_processor
def inject_user_cash():
    """Make user cash available on all pages (for top-right display)."""
    if "user_id" in session:
        user_id = session["user_id"]
        # Query the user's available cash from the database
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        if user_cash:
            return {"user_cash": usd(user_cash[0]["cash"])}
    return {"user_cash": None}


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Get user's cash
    user_cash_data = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    user_cash = user_cash_data[0]["cash"] if user_cash_data else 0

    # Fetch stock portfolio data with latest prices
    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM purchases WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    # Preparing your portfolio data with prices and total values
    finance = []
    for row in rows:
        quote = lookup(row["symbol"])  # Fetch current stock price
        # Calculating total value for the stock in portfolio
        total_value = quote["price"] * row["total_shares"]
        finance.append({
            "symbol": row["symbol"],
            "total_shares": row["total_shares"],
            "price": quote["price"],
            "timestamp": row.get("timestamp"),
            "total_value": total_value
        })

    return render_template("index.html", finance=finance, user_cash=usd(user_cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session["user_id"]

    # Get user's available cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        # Validate stock lookup
        if stock is None:
            return apology("Invalid Symbol")

        shares = request.form.get("shares")

        # Validate shares input
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid amount of shares.")

        total_cost = stock["price"] * int(shares)

        # Checking if user has enough cash
        if total_cost > user_cash:
            return apology("Not enough cash")

        # Log the purchase in the purchases table
        db.execute(
            "INSERT INTO purchases (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
            user_id, symbol, shares, stock["price"], datetime.now()
        )

        # Updating user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)

        flash(
            f"Bought {shares} of {symbol} for {usd(total_cost)}, Updated cash: {usd(user_cash - total_cost)}")
        return redirect("/")

    return render_template("buy.html", user_cash=usd(user_cash))


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()  # Keep using 'symbol' for purchases
        shares = request.form.get("shares")

        # Validate shares input
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Shares must be a positive integer")

        # Lookup user's shares for the symbol in the purchases table
        user_shares = db.execute("SELECT SUM(shares) as total_shares FROM purchases WHERE user_id = ? AND symbol = ?",
                                 user_id, symbol)[0]["total_shares"]

        if user_shares is None or user_shares < int(shares):
            return apology("Not enough shares")

        # Looking up information about the stock if it exists
        stock = lookup(symbol)
        if stock is None:
            return apology("Symbol does not exist")

        # Calculate total sale value
        total_value = stock["price"] * int(shares)

        # Log the sale in the purchases table
        db.execute(
            "INSERT INTO purchases (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
            # Logging the sale as negative
            user_id, symbol, -int(shares), stock["price"], datetime.now()
        )

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)

        flash(f"Sold {shares} of {symbol} for {usd(total_value)}")
        return redirect("/")

    # Handle GET request
    stocks = db.execute("SELECT symbol FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)
    return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    history = db.execute("SELECT symbol, shares, price, timestamp, type FROM purchases WHERE user_id = ? ORDER BY timestamp DESC",
                         user_id)
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Getting the symbol and then removing any whitespace
        symbol = request.form.get("symbol").strip()
        if not symbol:  # Check if the symbol is empty or not.
            return apology("Ticker symbol cannot be blank", 400)
        quote = lookup(symbol)
        if quote is None:
            return apology("Invalid Quote", 400)
        return render_template("quoted.html", quote=quote)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match.")

        hashed_password = generate_password_hash(request.form.get("password"))
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       request.form.get("username"), hashed_password)
        except:
            return apology("Username already exists", 400)

        return redirect("/login")
    return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password"""
    if request.method == "POST":
        user_id = session["user_id"]

        # Get the current password and new password from the form
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Validate input
        if not current_password or not new_password or not confirm_password:
            return apology("All fields are required.")

        # Check if the new passwords match
        if new_password != confirm_password:
            return apology("New passwords do not match.")

        # Get the user's hashed password from the database
        user = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if len(user) != 1 or not check_password_hash(user[0]["hash"], current_password):
            return apology("Current password is incorrect.")

        # Hash the new password and update it in the database
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, user_id)

        # Redirect to homepage or another page after password change
        return redirect("/")

    return render_template("change_password.html")  # Render the change password form
