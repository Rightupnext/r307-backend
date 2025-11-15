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

    # ? Reload full user from DB by ID
    user = User.objects.get(id=user.id)

    return jsonify({
        "match": True,
        "score": score,
        "user": {
            "id": str(user.id),

            # Personal details
            "bioMetricID": user.bioMetricID,
            "firstName": user.firstName,
            "middleName": user.middleName,
            "lastName": user.lastName,
            "fatherName": user.fatherName,
            "chestNo": user.chestNo,
            "rollNo": user.rollNo,
            "email": user.email,
            "dateOfBirth": user.dateOfBirth.isoformat() if user.dateOfBirth else None,
            "age": user.age,
            "mobileNumber": user.mobileNumber,
            "mobileNumber2": user.mobileNumber2,
            "eduQualification": user.eduQualification,
            "manual_create_date": user.manual_create_date,
            "aadharNumber": user.aadharNumber,
            "identificationMarks_1": user.identificationMarks_1,
            "identificationMarks_2": user.identificationMarks_2,
            "village": user.village,
            "post": user.post,
            "tehsil": user.tehsil,
            "district": user.district,
            "state": user.state,
            "pincode": user.pincode,
            "trade": user.trade,
            "police_station": user.police_station,

            # Physical details
            "height": user.height,
            "weight": user.weight,
            "chest": user.chest,
            "run": user.run,
            "pullUp": user.pullUp,
            "balance": user.balance,
            "ditch": user.ditch,
            "medical": user.medical,
            "tradeTest": user.tradeTest,

            # Scoring
            "centerName": user.centerName,
            "centerCode": user.centerCode,
            "totalPhysical": user.totalPhysical,
            "totalMarks": user.totalMarks,

            # Files
            "photo": user.photo,

            # Fingerprint flags (safe)
            "finger1": True if user.finger1 else False,
            "finger2": True if user.finger2 else False,

            # System
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    })



@finger_bp.route("/scanner/stop", methods=["POST"])
def stop_scan():
    port = _get_port()
    sensor_manager.register_port(port)
    stop_fingerprint_scan(port)
    return jsonify({"status": "stopped", "port": port})
@finger_bp.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        # Fetch user from MongoDB
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    # Prepare response
    return jsonify({
        "match": True,
        "user": {
            "id": str(user.id),

            # Personal details
            "bioMetricID": user.bioMetricID,
            "firstName": user.firstName,
            "middleName": user.middleName,
            "lastName": user.lastName,
            "fatherName": user.fatherName,
            "chestNo": user.chestNo,
            "rollNo": user.rollNo,
            "email": user.email,
            "dateOfBirth": user.dateOfBirth.isoformat() if user.dateOfBirth else None,
            "age": user.age,
            "mobileNumber": user.mobileNumber,
            "mobileNumber2": user.mobileNumber2,
            "eduQualification": user.eduQualification,
            "aadharNumber": user.aadharNumber,
            "identificationMarks_1": user.identificationMarks_1,
            "identificationMarks_2": user.identificationMarks_2,
            "manual_create_date": user.manual_create_date,
            "village": user.village,
            "post": user.post,
            "tehsil": user.tehsil,
            "district": user.district,
            "state": user.state,
            "pincode": user.pincode,
            "trade": user.trade,
            "police_station": user.police_station,

            # Physical details
            "height": user.height,
            "weight": user.weight,
            "chest": user.chest,
            "run": user.run,
            "pullUp": user.pullUp,
            "balance": user.balance,
            "ditch": user.ditch,
            "medical": user.medical,
            "tradeTest": user.tradeTest,

            # Scoring
            "centerName": user.centerName,
            "centerCode": user.centerCode,
            "totalPhysical": user.totalPhysical,
            "totalMarks": user.totalMarks,

            # Files
            "photo": user.photo,

            # Fingerprint flags (safe)
            "finger1": True if user.finger1 else False,
            "finger2": True if user.finger2 else False,

            # System
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    })