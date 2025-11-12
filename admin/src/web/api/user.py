from __future__ import annotations
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserReadSchema,
)
from src.models.auth import (
    email_exists,
    user_new,
    user_check_password,
    user_show,
)
from src.models.database import db
from src.models.auth.role import Role


# Este blueprint cuelga de /api (ver registro en src/web/__init__.py)
bp = Blueprint("user_api", __name__, url_prefix="/user")


@bp.post("/register")
def register_user():
    try:
        payload = UserCreateSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400

    if email_exists(payload["email"]):
        return jsonify(error="email ya registrado"), 409

    # Rol por defecto: editor
    role = db.session.query(Role).filter_by(name="editor").first()
    if role is None:
        return jsonify(error="rol por defecto 'editor' no está creado"), 500

    user = user_new(
        email=payload["email"],
        name=payload["name"],
        last_name=payload["last_name"],
        password=payload["password"],
        role_id=role.id,
    )

    return jsonify(UserReadSchema().dump(user)), 201


@bp.post("/login")
def login_user():
    try:
        payload = UserLoginSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400

    if not user_check_password(payload["email"], payload["password"]):
        return jsonify(error="credenciales invalidas"), 401

    user = user_show(payload["email"])  # para devolver datos mínimos
    return jsonify(user=UserReadSchema().dump(user), message="login ok"), 200

