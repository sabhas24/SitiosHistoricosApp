import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user_id: int) -> tuple[str, int]:
    """Genera un JWT para el usuario.
    
    Returns:
        tuple: (token, expires_in_seconds)
    """
    expiration = current_app.config["JWT_EXPIRATION_SECONDS"]
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
