from app.data import Data

class UserRepository:
    def __init__(self):
        self.db = Data()

    def get_all(self, page=1):
        query = "SELECT * FROM user WHERE is_active = 1"
        return self.db.get_data_lim(query, (), page)

    def insert(self, dto):
        query = """
            INSERT INTO user (username, email, is_active)
            VALUES (%s, %s, %s)
        """
        values = (dto.username, dto.email, dto.is_active)
        return self.db.insert_data(query, values)
