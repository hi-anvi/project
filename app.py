# Import modules
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required, apology

# Configure application session["contacts"]
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
db = SQL("sqlite:///project.db")

# Give error if page not found


@app.errorhandler(404)
def page_not_found(e):
    return apology("Page not found", 404)

# Define index page route


@app.route("/")
@login_required
def index():
    """Default page if logged in contacts"""
    return render_template("index.html")

# Allow user to register


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    if not username or not password1 or not password2:
        return apology("give needed info")
    if password1 != password2:
        return apology("passwords not the same")
    users = db.execute("SELECT username FROM users;")
    for name in users:
        if name["username"] == username:
            return apology("Username already used.")
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?);",
               username, generate_password_hash(password1))
    return redirect("/")

# Allow user to login


@app.route("/login", methods=["GET", "POST"])
def login():
    """Allow login"""
    # If user loads page, show form
    if request.method == "GET":
        return render_template("login.html")

    # Get password and username if user submited form
    username = request.form.get("username")
    password = request.form.get("password")

    # Make sure both username and password were typed
    if not username or not password:
        return apology("Please provide the specified input")

    # Check if username matches password
    users = db.execute("SELECT * FROM users WHERE username = ?;", username)
    if len(users) != 1 or not check_password_hash(users[0]["password_hash"], password):
        return apology("Invalid username or password")

    # If all clear, set stuff to be theirs
    session["user_id"] = users[0]["id"]
    session["username"] = users[0]["username"]
    session["tag"] = False

    # Get the contacts of the user
    contacts = db.execute(
        "SELECT * FROM text_pals WHERE user_id = ?;", session["user_id"])
    session["contacts"] = []
    for contact in contacts:
        session["contacts"].append(db.execute("SELECT * FROM users WHERE id = ?;",
                                              contact["pal_user_id"])[0]["username"])

    return redirect("/")

# Logout user


@app.route("/logout")
@login_required
def logout():
    """Logs out a user"""
    session.clear()
    return redirect("/")

# Allow user to change contacts and tags


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Allows user to change profile features"""

    # Show form if user loads page
    if request.method == "GET":
        return render_template("settings.html")

    # Get data
    username = request.form.get("username")
    new_tag = request.form.get("tag-add")
    if username:
        users = db.execute("SELECT * FROM users;")
        contacts = db.execute("SELECT * FROM text_pals WHERE user_id = ?;", session["user_id"])

        # Check if user exists and it is not in contacts
        username_exists = False
        in_contacts = False
        id = None
        for user in users:
            if user["username"] == username:
                username_exists = True
                id = db.execute("SELECT id FROM users WHERE username = ?;", username)[0]["id"]
                break
        for contact in contacts:
            if contact["pal_user_id"] == id:
                in_contacts = True

        # Final test
        if username_exists and not in_contacts:
            db.execute("INSERT INTO text_pals (user_id, pal_user_id) VALUES (?, ?);",
                       session["user_id"], id)
            db.execute("INSERT INTO text_pals (pal_user_id, user_id) VALUES (?, ?);",
                       session["user_id"], id)

            # Clear session for contacts to be updated
            session.clear()

        else:
            return apology("username not valid")
    elif new_tag:
        contact = request.form.get("account-add")
        con_id = db.execute("SELECT * FROM users WHERE username = ?;", contact)
        if not con_id:
            return apology("Invaild contact")
        contact_exists = db.execute(
            "SELECT * FROM text_pals WHERE user_id = ? AND pal_user_id = ?;", session["user_id"], con_id[0]["id"])
        contact_exists1 = db.execute(
            "SELECT * FROM text_pals WHERE user_id = ? AND pal_user_id = ?;", con_id[0]["id"], session["user_id"])
        if not contact_exists or not contact_exists1:
            return apology("Invalid contact")
        exist = db.execute(
            "SELECT tag FROM tags WHERE text_pal_id = ? AND tag = ?;", contact_exists[0]["id"], new_tag)
        if exist:
            return apology("tag already exists")
        db.execute("INSERT INTO tags (text_pal_id, tag) VALUES (?, ?);",
                   contact_exists[0]["id"], new_tag)
        db.execute("INSERT INTO tags (text_pal_id, tag) VALUES (?, ?);",
                   contact_exists1[0]["id"], new_tag)
    else:
        username = request.form.get("account")
        tag = request.form.get("tag")
        if not username or not tag or username == session["username"]:
            return apology("Invalid contact")
        id = db.execute("SELECT id FROM users WHERE username = ?;", username)
        if not id:
            return apology("invalid contact")
        text_pal_id = db.execute(
            "SELECT * FROM text_pals WHERE user_id = ? AND pal_user_id = ?;",
            session["user_id"], id[0]["id"])
        text_pal_id1 = db.execute(
            "SELECT * FROM text_pals WHERE user_id = ? AND pal_user_id = ?;",
            id[0]["id"], session["user_id"])
        print(text_pal_id)
        if not text_pal_id or not text_pal_id1:
            return apology("contact not found")
        tag_id = db.execute("SELECT * FROM tags WHERE text_pal_id = ? AND tag = ?;",
                            text_pal_id[0]["id"], tag)
        tag_id1 = db.execute("SELECT * FROM tags WHERE text_pal_id = ? AND tag = ?;",
                             text_pal_id1[0]["id"], tag)
        if not tag_id or not tag_id1:
            return apology("invalid tag or contact")
        db.execute("DELETE FROM tags WHERE id = ?;", tag_id[0]["id"])
        db.execute("DELETE FROM tags WHERE id = ?;", tag_id1[0]["id"])
        db.execute("DELETE FROM chat_history WHERE tag_id = ?;", tag_id[0]["id"])
        db.execute("DELETE FROM chat_history WHERE tag_id = ?;", tag_id1[0]["id"])

    return redirect("/")


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    """Shows the chat history to the user"""

    def get_tags():
        return db.execute("SELECT * FROM tags WHERE text_pal_id = ?;", session["text_pal_id"][0]["id"])

    def get_history():
        tag_id = db.execute("SELECT id FROM tags WHERE tag = ? AND text_pal_id = ?;",
                            session["tag"], session["text_pal_id"][0]["id"])
        if not tag_id:
            return []
        return db.execute(
            "SELECT * FROM chat_history WHERE tag_id = ? AND text_pal_id = ? ORDER BY timestamp;",
            tag_id[0]["id"], session["text_pal_id"][0]["id"])

    # Handle GET
    if request.method == "GET":
        contact = request.args.get("contacts")
        if not contact and not session.get("contact_id"):
            return apology("No selected user")
        if contact:
            user = db.execute(
                "SELECT id FROM users WHERE username = ?;", contact)
            contact_name = contact
            if not user:
                return apology("Contact not found")
            session["contact_id"] = user[0]["id"]
            text_pal = db.execute(
                "SELECT id FROM text_pals WHERE (user_id = ? AND pal_user_id = ?) OR (user_id = ? AND pal_user_id = ?);",
                session["user_id"], session["contact_id"], session["contact_id"], session["user_id"])
            if not text_pal:
                return apology("Text pal not found")
            session["text_pal_id"] = text_pal
        else:
            contact_name = db.execute("SELECT username FROM users WHERE id = ?;", session["contact_id"])[
                0]["username"]
        tags = get_tags()
        messages = get_history()
        if not session["tag"]:
            messages = []
        return render_template("chat.html", tags=tags, messages=messages, contact=contact_name)

    # Handle POST
    if "tag" in request.form:
        tag = request.form.get("tag")
        if not tag:
            return apology("no tag selected")
        session["tag"] = tag
        return redirect("/chat")

    if "message" in request.form:
        message = request.form.get("message")
        if not message:
            return apology("no message")
        if not session.get("tag") or not session.get("text_pal_id"):
            return apology("no tag or contact selected")
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tag_id = db.execute("SELECT * FROM tags WHERE tag = ? AND text_pal_id = ?;",
                            session["tag"], session["text_pal_id"][0]["id"])
        if not tag_id:
            return apology("Tag not found")
        tag_id = tag_id[0]["id"]
        db.execute(
            "INSERT INTO chat_history (text_pal_id, sender_id, receiver_id, timestamp, tag_id, message) VALUES (?, ?, ?, ?, ?, ?);",
            session["text_pal_id"][0]["id"], session["user_id"], session["contact_id"], time, tag_id, message)
        db.execute(
            "INSERT INTO chat_history (text_pal_id, sender_id, receiver_id, timestamp, tag_id, message) VALUES (?, ?, ?, ?, ?, ?);",
            session["text_pal_id"][1]["id"], session["user_id"], session["contact_id"], time, tag_id, message)
        return redirect("/chat")

    return apology("Invalid request")

############

# AI was used
# That is: Git Copilot

#############

# TODO list
# Set index page
# Set AI mode - later after submitting
# Make send message button on better location - CSS
