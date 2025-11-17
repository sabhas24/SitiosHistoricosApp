from flask import (
    Blueprint,
    request,
    jsonify,
    url_for,
    redirect,
    current_app,
    make_response,
    session,
)
from marshmallow import ValidationError
from src.web.schemas.user import UserCreateSchema, UserReadSchema, UserLoginSchema
from src.models.auth import email_exists, user_new, user_check_password, user_show
from src.models.auth.role import Role
from src.models.database import db
from os import environ
import secrets
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)

bp = Blueprint("user_api", __name__, url_prefix="/api/user")


def get_oauth():
    return current_app.extensions["authlib.integrations.flask_client"]


@bp.post("/register")
def register_user():
    """Registrar un nuevo usuario."""
    try:
        user_data = UserCreateSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400

    if email_exists(user_data["email"]):
        return jsonify(error="exists", message="El correo ya está registrado"), 400

    public_role = db.session.query(Role).filter_by(name="public_user").first()
    user = user_new(
        email=user_data["email"],
        name=user_data["name"],
        last_name=user_data["last_name"],
        password=user_data["password"],
        role=public_role,
    )
    user_read = UserReadSchema().dump(user)
    return jsonify(user_read), 201


@bp.post("/login")
def login_user():
    """Iniciar sesión y obtener token JWT."""
    try:
        login_data = UserLoginSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400

    if not user_check_password(login_data["email"], login_data["password"]):
        return (
            jsonify(
                error="invalid_credentials", message="Correo o contraseña incorrectos"
            ),
            401,
        )

    user = user_show(login_data["email"])
    access_token = create_access_token(identity=str(user.id))
    user_data = UserReadSchema().dump(user)

    response = jsonify({"user": user_data, "message": "Login exitoso"})

    set_access_cookies(response, access_token)

    return response, 200


@bp.get("/login/google")
def login_google():
    oauth = get_oauth()
    redirect_uri = url_for("api.user_api.login_callback", _external=True)
    nonce = secrets.token_urlsafe(16)
    session["nonce"] = nonce
    return oauth.google.authorize_redirect(redirect_uri=redirect_uri, nonce=nonce)


@bp.get("/login/callback")
def login_callback():
    try:
        oauth = get_oauth()
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token, nonce=session.get("nonce"))

        email = user_info["email"]
        name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")

        if not email_exists(email):
            public_role = db.session.query(Role).filter_by(name="public_user").first()
            user = user_new(
                email=email,
                name=name,
                last_name=last_name,
                password=f"oauth_{email}",
                role=public_role,
            )
        else:
            user = user_show(email)

        access_token = create_access_token(identity=str(user.id))

        frontend_base = current_app.config["FRONTEND_BASE_URL"]
        frontend_url = f"{frontend_base}/login-success"
        response = make_response(redirect(frontend_url))
        set_access_cookies(response, access_token)

        return response

    except Exception as e:
        return jsonify(error="oauth_error", message=str(e)), 400


@bp.post("/logout")
def logout_user():
    """Cerrar sesión del usuario."""
    try:
        response = make_response(jsonify(message="Logout exitoso"))
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify(error="logout_error", message=str(e)), 400
