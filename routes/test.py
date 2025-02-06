from flask import Blueprint, jsonify
from app import db

test_bp = Blueprint('test', __name__)

@test_bp.route('/test-db', methods=['GET'])
def test_db():
    try:
        # Basit bir veritabanı sorgusu
        result = db.session.execute("SELECT 1").fetchall()
        return jsonify({"message": "Database connection successful!", "result": str(result)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
