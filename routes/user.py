@app.route("/user-profile", methods=["GET"])
async def user_profile(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error": "Authorization header is missing"}, status=401)

    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status=401)

    return json({
        "message": f"Welcome, {decoded.get('username')}!",
        "role": decoded.get("role")
    })
