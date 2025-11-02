from flask import Blueprint, jsonify, request
from controllers.fingerprint_controller import enroll_fingerprint, verify_fingerprint, stop_fingerprint_scan
from utils.sensor_manager import sensor_manager
from utils.enroll_session import enroll_session
from models.user import User

finger_bp = Blueprint("finger_bp", __name__, url_prefix="/finger")


def _get_port():
    pid = request.args.get("port", 0, type=int)
    return f"/dev/ttyUSB{pid}"


@finger_bp.route("/enroll/finger1", methods=["POST"])
def enroll_finger1():
    port = _get_port()
    sensor_manager.register_port(port)

    result = enroll_fingerprint(port)

    if result["status"] != "success":
        return jsonify(result), 400

    enroll_session[port] = result["template_bytes"]

    return jsonify({
        "message": "Finger 1 captured",
        "finger1_template": result["template_b64"],
        "port": port
    })


@finger_bp.route("/enroll/finger2", methods=["POST"])
def enroll_finger2():
    port = _get_port()
    sensor_manager.register_port(port)

    if port not in enroll_session:
        return jsonify({"error": "Scan Finger 1 first"}), 400

    result = enroll_fingerprint(port)

    if result["status"] != "success":
        return jsonify(result), 400

    return jsonify({
        "message": "Finger 2 captured",
        "finger2_template": result["template_b64"],
        "port": port
    })


@finger_bp.route("/verify", methods=["GET"])
def verify_route():
    port = _get_port()
    sensor_manager.register_port(port)

    match, user, score = verify_fingerprint(port)

    if not match:
        return jsonify({"match": False, "message": "No match"}), 404

    return jsonify({
        "match": True,
        "score": score,
        "user": {
            "id": str(user.id),
            "firstName": user.firstName,
            "rollNo": user.rollNo,
            "chestNo": user.chestNo,
        }
    })


@finger_bp.route("/scanner/stop", methods=["POST"])
def stop_scan():
    port = _get_port()
    sensor_manager.register_port(port)
    stop_fingerprint_scan(port)
    return jsonify({"status": "stopped", "port": port})
