from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.user import UserCreateSchema, UserReadSchema, UserLoginSchema
from src.models.auth import email_exists, user_new, get_roleid_by_name, user_check_password, user_show
from src.web.utils.jwt_utils import generate_jwt_token

bp = Blueprint('user_api', __name__, url_prefix='/api/user')

@bp.post('/register')
def register_user():
    """Registrar un nuevo usuario."""
    try:
        user_data = UserCreateSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400
    
    if email_exists(user_data["email"]):
        return jsonify(error="exists", message="El correo ya está registrado"), 400
    
    user = user_new(
        email=user_data["email"],   
        name=user_data["name"],
        last_name=user_data["last_name"],
        password=user_data["password"],
        role=get_roleid_by_name("user")  
    )
    user_read = UserReadSchema().dump(user)
    return jsonify(user_read), 201


@bp.post('/login')
def login_user():
    """Iniciar sesión y obtener token JWT."""
    try:
        login_data = UserLoginSchema().load(request.get_json(force=True))
    except ValidationError as e:
        return jsonify(error="validacion", details=e.messages), 400
    
    if not user_check_password(login_data["email"], login_data["password"]):
        return jsonify(error="invalid_credentials", message="Correo o contraseña incorrectos"), 401
    
    user = user_show(login_data["email"])
    user_read = UserReadSchema().dump(user)
    token, expires_in = generate_jwt_token(user.id)
    return jsonify(token=token, expires_in=expires_in, user=user_read), 200