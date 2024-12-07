import jwt
import datetime
from config import SECRET_KEY

def generate_token(user_id, username, role, expiration_hours=1):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def check_role(decoded_token, required_role):
    return decoded_token.get("role") == required_role

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
