from flask import Blueprint, jsonify
from src.models.feature_flag.feature_flag_services import are_reviews_enabled, is_portal_maintenance_active

bp_config = Blueprint("config_api", __name__)

@bp_config.get("/config")
def get_config():
    """Obtener configuración pública del sistema"""
    return jsonify({
        "reviews_enabled": are_reviews_enabled(),
        "portal_maintenance_mode": is_portal_maintenance_active()
    }), 200
