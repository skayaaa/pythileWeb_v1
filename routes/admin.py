@app.route("/admin-dashboard", methods=["GET"])
async def admin_dashboard(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error": "Authorization header is missing"}, status=401)

    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status=401)

    if not check_role(decoded, "admin"):
        return json({"error": "Access denied"}, status=403)

    return json({"message": "Welcome to admin dashboard!"})
