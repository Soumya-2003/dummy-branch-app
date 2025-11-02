from flask import Blueprint, jsonify
from sqlalchemy import text
from ..db import SessionContext

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        with SessionContext() as session:
            session.execute(text("SELECT 1"))
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "connection failed",
            "error": str(e)
        }), 500