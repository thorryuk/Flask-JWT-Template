class UserCreateDTO:
    def __init__(self, payload: dict):
        self.username = payload.get("username", "").strip()
        self.email = payload.get("email", "").strip()
        self.is_active = payload.get("is_active", 1)

    def validate(self):
        if not self.username:
            raise ValueError("username is required")

        if len(self.username) < 3:
            raise ValueError("username must be at least 3 characters")

        if "@" not in self.email:
            raise ValueError("invalid email format")
