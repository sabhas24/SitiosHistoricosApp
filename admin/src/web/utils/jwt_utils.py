import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps


def generate_jwt_token(user_id: int) -> tuple[str, int]:
    """Genera un JWT para el usuario.
    
    Returns:
        tuple: (token, expires_in_seconds)
    """
    expiration = current_app.config["JWT_EXPIRATION"]
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expiration),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )
    return token, expiration


def decode_token(token: str) -> dict | None:
    """Decodifica un JWT y retorna su payload.
    
    Returns:
        dict | None: Payload del token o None si es inválido o expirado.
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):
    """Decorator to protect routes with JWT authentication."""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"error": "authorization_header_missing"}), 401

        parts = auth_header.split()
        # validacion del formato del header
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({"error": "invalid_authorization_header"}), 401

        token = parts[1]
        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "invalid_or_expired_token"}), 401

        request.current_user_id = payload['user_id']
        return f(*args, **kwargs)

    return decorated_function
