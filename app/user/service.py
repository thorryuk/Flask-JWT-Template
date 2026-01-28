from .dto import UserCreateDTO
from .repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def list_users(self, page=1):
        return self.repo.get_all(page)
    
    def list_user_uuid(self, param):
        return self.repo.get_user_uuid(param)

    def create_user(self, payload: dict):
        dto = UserCreateDTO(payload)
        dto.validate()

        return self.repo.insert(dto)
