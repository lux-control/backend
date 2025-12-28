from flask import Blueprint, render_template
from ..auth.routes import login_required

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
@login_required
def landing_page():
    return render_template("base.html")