from flask import Blueprint, jsonify
from controllers.fingerprint_controller import capture_finger_template, verify_fingerprint,stop_fingerprint_scan

finger_bp = Blueprint('finger_bp', __name__)

@finger_bp.route("/capture/finger1", methods=["GET"])
def finger1():
    try:
        data = capture_finger_template(min_quality=60)

        if data["status"] == "low_quality":
            return jsonify(data), 400  # Bad Request � ask user to retry

        return jsonify({"finger1": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@finger_bp.route("/capture/finger2", methods=["GET"])
def finger2():
    try:
        data = capture_finger_template(min_quality=60)

        if data["status"] == "low_quality":
            return jsonify(data), 400

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

        # Convert Mongo user to JSON-like dict (exclude binary fingerprints)
        user_data = {
            "id": str(user.id),
            "firstName": user.firstName,
            "middleName": user.middleName,
            "lastName": user.lastName,
            "fatherName": user.fatherName,
            "chestNo": user.chestNo,
            "rollNo": user.rollNo,
            "email": user.email,
            "dateOfBirth": user.dateOfBirth.isoformat() if user.dateOfBirth else None,
            "mobileNumber": user.mobileNumber,
            "eduQualification": user.eduQualification,
            "aadharNumber": user.aadharNumber,
            "identificationMarks_1": user.identificationMarks_1,
            "identificationMarks_2": user.identificationMarks_2,
            "village": user.village,
            "post": user.post,
            "tehsil": user.tehsil,
            "district": user.district,
            "state": user.state,
            "pincode": user.pincode,
            "police_station": user.police_station,
            "trade": user.trade,
            "height": user.height,
            "weight": user.weight,
            "chest": user.chest,
            "run": user.run,
            "pullUp": user.pullUp,
            "balance": user.balance,
            "ditch": user.ditch,
            "medical": user.medical,
            "tradeTest": user.tradeTest,
            "centerName": user.centerName,
            "totalPhysical": user.totalPhysical,
            "totalMarks": user.totalMarks,
            "photo": user.photo,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }

        return jsonify({
            "match": True,
            "message": "Fingerprint Matched ?",
            "user": user_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ? STOP/RESET Scanner
@finger_bp.route("/scanner/stop", methods=["POST"])
def stop_scan():
    stop_fingerprint_scan()
    return jsonify({"status": "OK", "message": "Scanner stopped/reset ?"})