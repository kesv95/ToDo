
from flask import Blueprint, request, jsonify

from log.logger_config import action_logger


log_bp = Blueprint("log", __name__)


@log_bp.route("/api/log", methods=["POST"])
def save_action_log():
    """브라우저에서 전달된 사용자 행동을 로그 파일에 기록한다."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    action = data.get("action")
    target = data.get("target", "")

    allowed_actions = {
        "page_view",
        "click",
        "change",
        "submit"
    }

    if action not in allowed_actions:
        return jsonify({"error": "Invalid action"}), 400

    if not isinstance(target, str):
        return jsonify({"error": "Invalid target"}), 400

    target = target.replace("\r", " ").replace("\n", " ")[:100]

    action_logger.info(
        "action=%s target=%s",
        action,
        target
    )

    return jsonify({"success": True}), 200
