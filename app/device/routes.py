from flask import request, Blueprint
from ..auth.routes import login_required

device_bp = Blueprint("device", __name__, url_prefix="/device")

@device_bp.route("/monitor", methods=["GET"])
@login_required
def check_device():
    return "Device Screen"