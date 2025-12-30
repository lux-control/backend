from functools import wraps
from flask import Blueprint, url_for, session, redirect, render_template, request, abort
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from pathlib import Path
from flask import flash
from ..extensions import mongo
from ..user.model import User
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

REDIRECT_URI = os.getenv("REDIRECT_URI")

BASE_DIR = Path(__file__).resolve().parents[2]
client_secrets_file = BASE_DIR / "client_secret.json"

def build_flow(state=None):
    return Flow.from_client_secrets_file(
        client_secrets_file=str(client_secrets_file),
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
    )

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page", next=request.path))
        return function(*args, **kwargs)
    return wrapper


@auth_bp.route("/login", methods=["GET"])
def login_page():
    next_url = request.args.get("next", "/")
    return render_template("login.html", next=next_url)

@auth_bp.route("/register", methods=["GET"])
def register_page():
    next_url = request.args.get("next", "/")
    return render_template("register.html", next=next_url)


@auth_bp.route("/login/google", methods=["GET"])
def login_google():
    flow = build_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    session["state"] = state
    session["next"] = request.args.get("next", "/")
    return redirect(authorization_url)

@auth_bp.route("/login/local", methods=["POST"])
def login_local():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    next_url = request.form.get("next") or url_for("main.landing_page")

    if not email or not password:
        flash("Credentials missing")
        return redirect(url_for("auth.login_page", next=next_url))

    user = User.get_by_email(mongo.db, email)

    if not user or not User.verify_password(user.password, password):
        flash("Invalid credentials")
        return redirect(url_for("auth.login_page", next=next_url))

    session.clear()
    session["user_id"] = str(user._id)
    session["name"] = user.username
    session["email"] = email
    session["auth_provider"] = "local"

    return redirect(next_url)

@auth_bp.route("/register/local", methods=["POST"])
def register_local():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    next_url = request.form.get("next") or url_for("main.landing_page")

    if not email or not password or not username:
        flash("Credentials missing")
        return redirect(url_for("auth.register_page", next=next_url))

    existing = User.get_by_email(mongo.db, email)
    if existing:
        flash("User is already registered")
        return redirect(url_for("auth.login_page", next=next_url))

    user = User(
        device_id="testdeviceid", # TODO  change the hardcoded id 
        email=email,
        username=username,
        password=password,  # let save() hash
    )
    user.save()

    session.clear()
    session["user_id"] = str(user._id)
    session["name"] = user.username
    session["email"] = user.email
    session["auth_provider"] = "local"

    return redirect(next_url)

@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/callback", methods=["GET"])
def callback():
    state_in_session = session.get("state")
    state_in_request = request.args.get("state")

    if not state_in_session or state_in_session != state_in_request:
        abort(400, description="State mismatch. Try logging in again.")

    flow = build_flow(state=state_in_session)
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    info = id_token.verify_oauth2_token(
        credentials.id_token,
        GoogleRequest(),
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=10,
    )

    next_url = session.get("next") or url_for("main.landing_page")
    session.clear()

    session["user_id"] = info["sub"]
    session["name"] = info.get("name")
    session["email"] = info.get("email")
    session["auth_provider"] = "google"

    return redirect(next_url)
