from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "24032010"  # Secret key for session management

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect("feelings.db")  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form

        if not username:
            return render_template("register.html", error="Please enter a username")  # Return error if username is missing
        if not password:
            return render_template("register.html", error="Please enter a password")  # Return error if password is missing

        # Hash the password
        hash = generate_password_hash(password)

        # Save user details to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))  # Insert user details into database
            conn.commit()
            user_id = cursor.lastrowid  # Get the ID of the newly created user
            session["user_id"] = user_id  # Save user ID in the session
            session["username"] = username  # Save username in the session
            flash("Registration successful!")  # Flash success message
            return redirect(url_for('presentation'))  # Redirect to presentation page
        except sqlite3.IntegrityError:
            return render_template("register.html", error="This username is already taken")  # Return error if username is taken
        finally:
            conn.close()  # Close the database connection

    return render_template("register.html")  # Render registration page for GET request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")  # Get username from form
        password = request.form.get("password")  # Get password from form

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()  # Fetch user details from database
        conn.close()

        if user is None:
            return render_template("login.html", error="Invalid username or password")  # Return error if user not found

        if not check_password_hash(user["hash"], password):
            return render_template("login.html", error="Invalid username or password")  # Return error if password is incorrect

        session["user_id"] = user["id"]  # Save user ID in the session
        session["username"] = user["username"]  # Save username in the session
        flash("Login successful!")  # Flash success message
        return redirect(url_for('presentation'))  # Redirect to presentation page

    return render_template("login.html")  # Render login page for GET request

@app.route("/presentation", methods=["GET", "POST"])
def presentation():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")  # Redirect if not logged in
    return render_template("presentation.html", user_id=user_id)

def save_feeling(user_id, feeling):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO user_feelings (user_id, feeling) VALUES (?, ?)",
        (user_id, feeling)
    )
    conn.commit()
    conn.close()

@app.route("/bad", methods=["POST"])
def bad():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")  # Redirect if user is not logged in

    # Save the feeling
    save_feeling(user_id, "Not well at all")

    # Render the bad.html page
    return render_template("bad.html", suggest="Hang in there, things will get better")

@app.route("/great", methods=["POST"])
def great():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")  # Redirect if user is not logged in

    save_feeling(user_id, "Great")
    return render_template("great.html", suggest="Excellent!")

@app.route("/ok", methods=["POST"])
def ok():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")  # Redirect if user is not logged in

    save_feeling(user_id, "Just ok")
    return render_template("ok.html", suggest="You are capable of amazing things")

@app.route("/not_ok", methods=["POST"])
def not_ok():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")  # Redirect if user is not logged in

    save_feeling(user_id, "Not so well")
    return render_template("not_ok.html", suggest="It's okay to feel down sometimes")

@app.route("/history", methods=["GET"])
def history():
    """Show history of feelings"""
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/")  # Redirect if not logged in

    conn = get_db_connection()
    feelings = conn.execute(
        "SELECT time, feeling FROM user_feelings WHERE user_id = ? ORDER BY time DESC",
        (user_id,)
    ).fetchall()
    conn.close()

    return render_template("history.html", feelings=feelings)

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode
