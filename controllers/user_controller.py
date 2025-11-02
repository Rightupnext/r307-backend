from flask import request, jsonify, Response
from models.user import User
import os, base64, datetime, pytz, time
import base64
from bson import ObjectId

# Folder paths
BASE_DIR = "/home/siva"
UPLOAD_PHOTO_DIR = os.path.join(BASE_DIR, "photos")
UPLOAD_FINGER_DIR = os.path.join(BASE_DIR, "fingerprint")

os.makedirs(UPLOAD_PHOTO_DIR, exist_ok=True)
os.makedirs(UPLOAD_FINGER_DIR, exist_ok=True)

def create_user():
    try:
        # ? Optional user limit remove if not needed
        # if User.objects.count() >= 20:
        #     return jsonify({"error": "User limit reached (20)"}), 403

        data = request.form
        photo_file = request.files.get("photo")

        # ? Fingerprints (optional base64)
        finger1_b64 = data.get("finger1")
        finger2_b64 = data.get("finger2")

        finger1_bin = base64.b64decode(finger1_b64) if finger1_b64 else None
        finger2_bin = base64.b64decode(finger2_b64) if finger2_b64 else None

        # ? rollNo optional
        roll = data.get("rollNo") or ""

        # ? Save photo (optional)
        photo_name = None
        if photo_file:
            file_prefix = roll if roll else str(int(time.time()))
            photo_name = f"{file_prefix}_photo.jpg"
            photo_file.save(os.path.join(UPLOAD_PHOTO_DIR, photo_name))

        # ? Timezone
        ist = pytz.timezone("Asia/Kolkata")
        now = datetime.datetime.now(ist)

        # ? Create user (all fields optional)
        user = User(
            firstName=data.get("firstName") or "",
            middleName=data.get("middleName") or "",
            lastName=data.get("lastName") or "",
            fatherName=data.get("fatherName") or "",
            chestNo=data.get("chestNo") or "",
            rollNo=roll,
            email=data.get("email") or "",
            age=data.get("age") or "",
            dateOfBirth=data.get("dateOfBirth") or None,
            mobileNumber=data.get("mobileNumber") or "",
            mobileNumber2=data.get("mobileNumber2") or "",
            eduQualification=data.get("eduQualification") or "",
            aadharNumber=data.get("aadharNumber") or "",
            identificationMarks_1=data.get("identificationMarks_1") or "",
            identificationMarks_2=data.get("identificationMarks_2") or "",
            village=data.get("village") or "",
            post=data.get("post") or "",
            tehsil=data.get("tehsil") or "",
            district=data.get("district") or "",
            state=data.get("state") or "",
            pincode=data.get("pincode") or "",
            trade=data.get("trade") or "",
            police_station=data.get("police_station") or "",
            height=data.get("height") or "",
            weight=data.get("weight") or "",
            chest=data.get("chest") or "",
            run=data.get("run") or "",
            pullUp=data.get("pullUp") or "",
            balance=data.get("balance") or "",
            ditch=data.get("ditch") or "",
            medical=data.get("medical") or "",
            tradeTest=data.get("tradeTest") or "",
            centerName=data.get("centerName") or "",
            totalPhysical=data.get("totalPhysical") or "",
            totalMarks=data.get("totalMarks") or "",
            photo=photo_name,
            finger1=finger1_bin,
            finger2=finger2_bin,
            created_at=now,
            updated_at=now
        )

        user.save()
        return jsonify({"message": "User created successfully", "id": str(user.id)}), 201

    except Exception as e:
        print("User create error:", e)
        return jsonify({"error": str(e)}), 500

def serialize_user(user):
    data = user.to_mongo().to_dict()

    # Convert Mongo ObjectId to string
    data["_id"] = str(data["_id"])

    # Convert datetime fields
    if "created_at" in data and data["created_at"]:
        data["created_at"] = data["created_at"].isoformat()

    if "updated_at" in data and data["updated_at"]:
        data["updated_at"] = data["updated_at"].isoformat()

    # Convert Binary fingerprint fields ? base64 string
    if "finger1" in data and data["finger1"]:
        data["finger1"] = base64.b64encode(data["finger1"]).decode()

    if "finger2" in data and data["finger2"]:
        data["finger2"] = base64.b64encode(data["finger2"]).decode()

    return data


def get_user(id):
    try:
        user = User.objects.get(id=id)
        return jsonify({"user": serialize_user(user)}), 200
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_users():
    try:
        users = [serialize_user(u) for u in User.objects()]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# Update User (correct fingerprint update)
def update_user(id):
    try:
        user = User.objects.get(id=id)

        data = request.form

        photo_file = request.files.get("photo")
        finger1_b64 = data.get("finger1")
        finger2_b64 = data.get("finger2")

        update_data = {}

        # ? Normal text fields update
        for key, value in data.items():
            if key not in ["finger1", "finger2"]:  # avoid overwrite raw binary
                update_data[key] = value

        # ? Fingerprint update ONLY if new scanned
        if finger1_b64:
            update_data["finger1"] = base64.b64decode(finger1_b64)

        if finger2_b64:
            update_data["finger2"] = base64.b64decode(finger2_b64)

        # ? Photo update only if new photo uploaded
        if photo_file:
            photo_name = f"{user.rollNo}_photo.jpg"
            photo_file.save(os.path.join(UPLOAD_PHOTO_DIR, photo_name))
            update_data["photo"] = photo_name

        # ? Update timestamp
        update_data["updated_at"] = datetime.datetime.utcnow()

        User.objects(id=id).update(**update_data)

        return jsonify({
            "message": "User updated successfully",
            "updatedFields": list(update_data.keys())
        }), 200

    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print("Update error:", e)
        return jsonify({"error": str(e)}), 500



# Delete User
def delete_user(id):
    try:
        User.objects.get(id=id).delete()
        return jsonify({"message": "User deleted successfully"})
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
