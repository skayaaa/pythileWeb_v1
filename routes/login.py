from utils.auth_utils import generate_token

MOCK_USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "user": {"password": "1234", "role": "user"}
}

def authenticate_user(username: str, password: str):
    user = MOCK_USERS.get(username)
    if not user or user["password"] != password:
        return None, "Invalid username or password"

    token = generate_token(user_id=1, username=username, role=user["role"])
    return token, None
