from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from user import db, User
from pokemon import Pokemon, add_pokemon_for_user
from datetime import timedelta
from hunt import Hunt, add_hunt_for_user

app = Flask(__name__)
app.secret_key = "naruto_beats_sasuke_as_adults"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Set cookie expiry for 30 days to retain login info.
app.permanent_session_lifetime = timedelta(days=30)


# =========== Routes ==========
"""
@route: Index or /
Handles pokemon search and base shiny tracking. Redirect to login if no
user currently logged in.

@method GET: Render index page
@method POST: Handles 3 buttons integration with shiny tracking being searching for pokemon and quering the 
database, incrementing the encounters, and resetting the encounters to 0.

@params: None
@returns: flask redirect(login) or flask render_template(index.html)
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if "id" not in session:
        return redirect(url_for("login"))

    pokemon_data = None
    hunt_data = None

    pokemon_name = None

    # Handle search
    if request.method == "POST":
        if "search_btn" in request.form:
            pokemon_name = request.form.get("pokemon_search", "").strip().lower()
            session["current_pokemon"] = pokemon_name

    # Fallback to last searched Pokémon
    if not pokemon_name:
        pokemon_name = session.get("current_pokemon")

    if pokemon_name:
        pokemon = add_pokemon_for_user(session["id"], pokemon_name)
        if pokemon:
            hunt = add_hunt_for_user(session["id"], pokemon.id_no)
            pokemon_data = pokemon.to_dict()
            hunt_data = hunt.to_dict()

    return render_template(
        "index.html",
        pokemon=pokemon_data,
        hunt=hunt_data,
        username=session.get("username"),
    )


"""
@route: Login
Handle user login

@method GET: Render login page
@method POST: Validate username and password from form data.
        - If valid store user info in session and redirect to main index page.
        - If not valid, reload the login page and send an error explaining.

@params: None
@returns: flask redirect(index) or flask render_template(login.html)
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Set the session expiry to the 30 day delay.
            session.permanent = True
            # Store both username and ID in session
            session["username"] = username
            session["id"] = user.id
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


"""
@route: Register
Handle user registration

@method POST: Retrieves submitted username and password from the form, checks if currently in database
and if not registers data to the database and redirects to index. If user already exists reload login page.

@params: None
@returns: flask redirect(index) or flask render_template(login.html)
"""


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("login.html", error="User already exists")
    else:
        new_user = User(username=username)  # type: ignore
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        # Store ID in session for new user
        session["username"] = username
        session["id"] = new_user.id
        return redirect(url_for("index"))


"""
@route: Logout
Handle user logout removing user data from the active session and reprompts for user login.

@params: None
@returns: flask redirect(login)
"""


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("id", None)
    return redirect(url_for("login"))


@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()
    pokemon_name = data["pokemon_name"]
    action = data["action"]
    hunt = None
    user_id = session.get("id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    pokemon = Pokemon.query.filter_by(user_id=user_id, name=pokemon_name).first()
    if pokemon:
        hunt = Hunt.query.filter_by(user_id=user_id, pokemon_id=pokemon.id_no).first()

    if hunt:
        if action == "increment":
            hunt.increment()
            db.session.commit()
        elif action == "reset":
            hunt.reset_count()
            db.session.commit()
        return jsonify({"encounters": hunt.encounters})
    else:
        return jsonify({"error", "Hunt not found."}), 404


# ======= App __init__ =========
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
