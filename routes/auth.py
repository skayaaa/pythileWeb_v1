from sanic import Blueprint, response
from utils.auth_utils import generate_token, decode_token, check_role
from sanic.response import json

auth_bp = Blueprint("auth", url_prefix="/auth")

MOCK_USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "user": {"password": "1234", "role": "user"}
}

@auth_bp.route("/login", methods=["POST"])
async def login(request):
    body = request.json
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return json({"error": "Username and password are required"}, status=400)

    user = MOCK_USERS.get(username)
    if not user or user["password"] != password:
        return json({"error": "Invalid username or password"}, status=401)

    role = user["role"]
    token = generate_token(user_id=1, username=username, role=role)  
    return json({"token": token}, status=200)


@auth_bp.route("/verify", methods=["POST"])
async def verify_token(request):
    body = request.json
    token = body.get("token")

    if not token:
        return json({"error": "Token is required"}, status=400)

    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status=401)

    return json({"decoded_token": decoded}, status=200)


@auth_bp.route("/admin-access", methods=["GET"])
async def admin_access(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error": "Authorization header is missing"}, status=401)

    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status=401)

    if not check_role(decoded, "admin"):
        return json({"error": "Access denied"}, status=403)

    return json({"message": "Welcome, admin!"}, status=200)
