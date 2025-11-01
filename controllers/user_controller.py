from flask import request, jsonify, Response
from models.user import User
import os, datetime, pytz

# Folder paths
BASE_DIR = "/home/siva"
UPLOAD_PHOTO_DIR = os.path.join(BASE_DIR, "photos")
UPLOAD_FINGER_DIR = os.path.join(BASE_DIR, "fingerprint")

os.makedirs(UPLOAD_PHOTO_DIR, exist_ok=True)
os.makedirs(UPLOAD_FINGER_DIR, exist_ok=True)

# Create User
def create_user():
    try:
        # Limit users (optional)
        if User.objects.count() >= 20:
            return jsonify({"error": "User limit reached (20)."}), 403

        data = request.form
        photo_file = request.files.get("photo")
        finger1_file = request.files.get("finger1")
        finger2_file = request.files.get("finger2")

        photo_name = None
        finger1_name = None
        finger2_name = None

        roll = data.get("rollNo") or str(datetime.datetime.utcnow().timestamp())

        # Photo Save
        if photo_file:
            photo_name = f"{roll}_photo.jpg"
            photo_file.save(os.path.join(UPLOAD_PHOTO_DIR, photo_name))

        # Fingerprint 1 Save
        if finger1_file:
            finger1_name = f"{roll}_finger1.bin"
            finger1_file.save(os.path.join(UPLOAD_FINGER_DIR, finger1_name))

        # Fingerprint 2 Save
        if finger2_file:
            finger2_name = f"{roll}_finger2.bin"
            finger2_file.save(os.path.join(UPLOAD_FINGER_DIR, finger2_name))

        ist = pytz.timezone("Asia/Kolkata")
        now = datetime.datetime.now(ist)

        user = User(
            firstName=data.get("firstName"),
            middleName=data.get("middleName"),
            lastName=data.get("lastName"),
            fatherName=data.get("fatherName"),
            chestNo=data.get("chestNo"),
            rollNo=roll,
            email=data.get("email"),
            mobileNumber=data.get("mobileNumber"),
            eduQualification=data.get("eduQualification"),
            aadharNumber=data.get("aadharNumber"),
            identificationMarks_1=data.get("identificationMarks_1"),
            identificationMarks_2=data.get("identificationMarks_2"),
            village=data.get("village"),
            post=data.get("post"),
            tehsil=data.get("tehsil"),
            district=data.get("district"),
            state=data.get("state"),
            pincode=data.get("pincode"),
            height=data.get("height"),
            weight=data.get("weight"),
            chest=data.get("chest"),
            run=data.get("run"),
            pullUp=data.get("pullUp"),
            balance=data.get("balance"),
            ditch=data.get("ditch"),
            medical=data.get("medical"),
            tradeTest=data.get("tradeTest"),
            centerName=data.get("centerName"),
            totalPhysical=data.get("totalPhysical"),
            totalMarks=data.get("totalMarks"),
            photo=photo_name,
            finger_Template_id=finger1_name,
            finger_Template_id_2=finger2_name,
            created_at=now,
            updated_at=now
        )

        user.save()

        return jsonify({"message": "User created successfully", "id": str(user.id)}), 201

    except Exception as e:
        print("User create error:", e)
        return jsonify({"error": str(e)}), 500


# Get All Users
def get_users():
    try:
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Get Single User
def get_user(id):
    try:
        user = User.objects.get(id=id)
        return Response(user.to_json(), mimetype="application/json", status=200)
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Update User (partial update allowed)
def update_user(id):
    try:
        data = request.form.to_dict() if request.form else request.json

        # Update timestamp
        data["updated_at"] = datetime.datetime.utcnow()

        User.objects.get(id=id).update(**data)
        return jsonify({"message": "User updated successfully"})
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Delete User
def delete_user(id):
    try:
        User.objects.get(id=id).delete()
        return jsonify({"message": "User deleted successfully"})
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
