from flask import Blueprint
from controllers.user_controller import (
    create_user, get_users, get_user, update_user, delete_user
)

user_bp = Blueprint("users", __name__)

@user_bp.route("/create", methods=["POST"])
def create_user_route():
    return create_user()

@user_bp.route("/", methods=["GET"])
def get_users_route():
    return get_users()

@user_bp.route("/<id>", methods=["GET"])
def get_user_route(id):
    return get_user(id)

@user_bp.route("/update/<id>", methods=["PUT"])
def update_user_route(id):
    return update_user(id)

@user_bp.route("/<id>", methods=["DELETE"])
def delete_user_route(id):
    return delete_user(id)


