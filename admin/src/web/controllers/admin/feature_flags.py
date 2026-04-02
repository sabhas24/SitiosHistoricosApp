from flask import render_template, request, jsonify, Blueprint, flash, redirect, url_for
from src.web.handlers.auth import check_permission, check
from src.models.feature_flag.feature_flag_services import (
    get_all_feature_flags,
    update_feature_flag,
    get_feature_flag_by_name,
)

feature_flags_bp = Blueprint(
    "feature_flags", __name__, url_prefix="/admin/feature-flags"
)


@feature_flags_bp.route("/")
@check("feature_flags")
def index():
    """Listado de feature flags - Solo para System Admins"""

    flags = get_all_feature_flags()
    return render_template("admin/feature_flags/index.html", flags=flags)


@feature_flags_bp.route("/toggle/<flag_name>", methods=["POST"])
@check("feature_flags")
def toggle_flag(flag_name):
    """Cambiar estado de un feature flag"""

    try:
        data = request.get_json()
        is_enabled = data.get("is_enabled", False)
        maintenance_message = data.get("maintenance_message", "")

        success, message = update_feature_flag(
            flag_name, is_enabled, maintenance_message
        )

        if success:
            return jsonify(
                {"success": True, "message": message, "is_enabled": is_enabled}
            )
        else:
            return jsonify({"success": False, "message": message}), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@feature_flags_bp.route("/get/<flag_name>")
@check("feature_flags")
def get_flag(flag_name):
    """Obtener información de un feature flag específico"""

    flag = get_feature_flag_by_name(flag_name)
    if not flag:
        return jsonify({"success": False, "message": "Flag no encontrado"}), 404

    return jsonify({"success": True, "flag": flag.to_dict()})
