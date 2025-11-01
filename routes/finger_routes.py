from flask import Blueprint, jsonify
from controllers.fingerprint_controller import capture_finger_template, verify_fingerprint,stop_fingerprint_scan

finger_bp = Blueprint('finger_bp', __name__)

# ? Capture Finger Template 1
@finger_bp.route("/capture/finger1", methods=["GET"])
def finger1():
    try:
        data = capture_finger_template()
        return jsonify({"finger1": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ? Capture Finger Template 2
@finger_bp.route("/capture/finger2", methods=["GET"])
def finger2():
    try:
        data = capture_finger_template()
        return jsonify({"finger2": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ? Verify Fingerprint
@finger_bp.route("/verify/finger", methods=["GET"])
def verify_finger():
    try:
        match, user = verify_fingerprint()

        if not match:
            return jsonify({"match": False, "message": "No match found!"}), 404

        return jsonify({
            "match": True,
            "message": "Fingerprint Matched ?",
            "user": {
                "id": str(user.id),
                "firstName": user.firstName,
                "middleName": user.middleName,
                "lastName": user.lastName,
                "fatherName": user.fatherName,
                "rollNo": user.rollNo,
                "chestNo": user.chestNo,
                "mobileNumber": user.mobileNumber,
                "village": user.village,
                "district": user.district,
                "state": user.state,
                "centerName": user.centerName,
                "totalPhysical": user.totalPhysical,
                "totalMarks": user.totalMarks,
                "photo": user.photo
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ? STOP/RESET Scanner
@finger_bp.route("/scanner/stop", methods=["POST"])
def stop_scan():
    stop_fingerprint_scan()
    return jsonify({"status": "OK", "message": "Scanner stopped/reset ?"})