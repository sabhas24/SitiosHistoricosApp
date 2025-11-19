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
        # Try Authorization header first
        auth_header = request.headers.get('Authorization', None)
        token = None

        if auth_header:
            parts = auth_header.split()
            # validacion del formato del header
            if parts[0].lower() == 'bearer' and len(parts) == 2:
                token = parts[1]
            else:
                return jsonify({"error": "invalid_authorization_header"}), 401
        else:
            # Fallback: check cookie (used by frontend with withCredentials)
            cookie_name = current_app.config.get('ACCESS_COOKIE_NAME', 'access_token_cookie')
            token = request.cookies.get(cookie_name)
            if not token:
                return jsonify({"error": "authorization_missing"}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "invalid_or_expired_token"}), 401

        # Extract user id from common JWT claim names
        user_id = None
        if isinstance(payload, dict):
            for key in ('user_id', 'user', 'sub', 'identity'):
                if key in payload:
                    user_id = payload[key]
                    break
            # Sometimes flask_jwt_extended stores identity under 'sub' or nested
            if user_id is None and isinstance(payload.get('identity'), dict):
                user_id = payload['identity'].get('user_id')

        if user_id is None:
            return jsonify({"error": "invalid_or_expired_token"}), 401

        # Normalize user_id to int when possible
        try:
            request.current_user_id = int(user_id)
        except Exception:
            request.current_user_id = user_id
        return f(*args, **kwargs)

    return decorated_function
