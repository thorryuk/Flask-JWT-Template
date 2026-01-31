from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin
from .service import AuthService

auth = Blueprint("auth", __name__)
service = AuthService()

@auth.route("/login", methods=["POST"])
@cross_origin()
def login():
    try:
        payload = request.json
        service.login(payload)
        return jsonify({"status": "success"})
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 400)
    except Exception as e:
        return make_response(jsonify({"error": "internal error"}), 500)
