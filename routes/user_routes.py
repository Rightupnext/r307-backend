from flask import Blueprint
from controllers.user_controller import (
    create_user, get_users, get_user, update_user, delete_user
)

user_bp = Blueprint("users", __name__)

user_bp.post("/")(create_user)
user_bp.get("/")(get_users)
user_bp.get("/<id>")(get_user)
user_bp.put("/<id>")(update_user)
user_bp.delete("/<id>")(delete_user)

