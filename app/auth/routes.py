from functools import wraps
from flask import Blueprint, url_for, session, redirect, render_template, request, abort
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from pathlib import Path

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

GOOGLE_CLIENT_ID = "447118152746-deui3vv85rjauma7gb26arqjul9urn80.apps.googleusercontent.com"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

REDIRECT_URI = "http://127.0.0.1:5000/auth/callback"

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
        if "google_id" not in session:
            return redirect(url_for("auth.login_page", next=request.path))
        return function(*args, **kwargs)
    return wrapper


@auth_bp.route("/login", methods=["GET"])
def login_page():
    next_url = request.args.get("next", "/")
    return render_template("login.html", next=next_url)


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

@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    pass

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

    session["google_id"] = info["sub"]
    session["name"] = info.get("name")
    session["email"] = info.get("email")

    return redirect(session.pop("next", "/"))