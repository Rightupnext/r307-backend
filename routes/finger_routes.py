# routes/fingerprint_routes.py
from flask import Blueprint, jsonify, request
from controllers.fingerprint_controller import enroll_fingerprint, verify_fingerprint, stop_fingerprint_scan
from models.user import User
from utils.sensor_manager import sensor_manager
from utils.enroll_session import enroll_session

finger_bp = Blueprint('finger_bp', __name__, url_prefix="/finger")

def _get_port():
    pid = request.args.get("port", default=0, type=int)
    return f"/dev/ttyUSB{pid}"

### ? ENROLL FINGER 1 � create new user globally
@finger_bp.route("/enroll/finger1", methods=["POST"])
def enroll_finger1():
    port = _get_port()
    sensor_manager.register_port(port)

    result = enroll_fingerprint(port)
    if result.get("status") != "success":
        return jsonify(result), 400

    # create new user
    user = User()
    user.finger1 = result["template"]
    user.save()

    # store enroll session for this port
    enroll_session[port] = str(user.id)

    return jsonify({
        "message": "Finger 1 stored successfully!",
        "person_id": str(user.id),
        "port": port
    }), 200


### ? ENROLL FINGER 2 � attach to same user
@finger_bp.route("/enroll/finger2", methods=["POST"])
def enroll_finger2():
    port = _get_port()
    sensor_manager.register_port(port)

    if port not in enroll_session:
        return jsonify({"error": "Finger1 not enrolled, session not found", "port": port}), 400

    user_id = enroll_session[port]
    user = User.objects.get(id=user_id)

    result = enroll_fingerprint(port)
    if result.get("status") != "success":
        return jsonify(result), 400

    user.finger2 = result["template"]
    user.save()

    # clear session
    enroll_session.pop(port, None)

    return jsonify({
        "message": "Finger 2 stored successfully!",
        "person_id": str(user.id),
        "port": port
    }), 200


### ? VERIFY FINGERPRINT � global match
@finger_bp.route("/verify", methods=["GET"])
def verify_finger_route():
    port = _get_port()
    sensor_manager.register_port(port)

    match, user, score = verify_fingerprint(port)

    if not match:
        return jsonify({"match": False, "message": "No match found", "port": port}), 404

    return jsonify({
        "match": True,
        "message": "Fingerprint Matched",
        "port": port,
        "score": score,
        "user": {
            "id": str(user.id),
            "firstName": getattr(user, "firstName", None),
            "chestNo": getattr(user, "chestNo", None),
            "rollNo": getattr(user, "rollNo", None),
        }
    }), 200


### ? STOP SCAN
@finger_bp.route("/scanner/stop", methods=["POST"])
def stop_scan():
    port = _get_port()
    sensor_manager.register_port(port)
    stop_fingerprint_scan(port)
    return jsonify({"status": "OK", "message": "Scanner stop attempted", "port": port}), 200
