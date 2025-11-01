from flask import request, jsonify, Response
from models.user import User
import json

# ? Create User
def create_user():
    try:
        data = request.json

        user = User(**data)
        user.save()

        return jsonify({"message": "User created successfully", "id": str(user.id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ? Get All Users
def get_users():
    try:
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ? Get Single User
def get_user(id):
    try:
        user = User.objects.get(id=id)
        return Response(user.to_json(), mimetype="application/json", status=200)

    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ? Update User
def update_user(id):
    try:
        data = request.json
        user = User.objects.get(id=id)

        user.update(**data)
        return jsonify({"message": "User updated successfully"}), 200

    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ? Delete User
def delete_user(id):
    try:
        user = User.objects.get(id=id)
        user.delete()

        return jsonify({"message": "User deleted successfully"}), 200

    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
