from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from .repository import AuthRepository

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username, password):
        user = self.repo.find_user_by_username(username)

        if not user:
            return None

        if not check_password_hash(user['password'], password):
            return None

        token = create_access_token(identity=user['id'])
        return token
