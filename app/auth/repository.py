from app.common.data import Data

class AuthRepository:
    def __init__(self):
        self.db = Data()

    def find_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        return self.db.get_data(query, (username, ))
    