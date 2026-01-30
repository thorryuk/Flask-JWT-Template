from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin
from .service import UserService

user = Blueprint("user", __name__)
service = UserService()

@user.route("/get", methods=["GET"])
@cross_origin()
def get_user():
    page = request.args.get("page", default=1, type=int)
    data = service.list_users(page)
    return jsonify({"data": data})

@user.route("/get/<user_uuid>", methods=["GET"])
@cross_origin()
def get_user_uuid(user_uuid):
    data = service.list_user_uuid(user_uuid)
    return jsonify({"data": data})

@user.route("/insert", methods=["POST"])
@cross_origin()
def insert_user():
    try:
        payload = request.json
        service.create_user(payload)
        return jsonify({"status": "success"})
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 400)
    except Exception as e:
        return make_response(jsonify({"error": "internal error"}), 500)
