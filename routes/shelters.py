from sanic import Blueprint, response
from models.shelters import Shelter
from sanic.response import json
from aiocache import cached , caches
from utils.auth_utils import decode_token

shelters_bp = Blueprint("shelters", url_prefix="/shelters")
@cached(ttl=60, key = "shelter_list")
async def get_shelters_list():
        shelters = await Shelter.all().values("id","name","location")
        return shelters 

@shelters_bp.route("/add", methods=["POST"])
async def add_shelter(request):
    
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error" : "Authorization header is missing"}, status = 401)
    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status = 401)
    if decoded.get("role") != "admin":
        return json({"error" : "Access denied"}, status = 401)
    
    data = request.json
    if not data:
        return json({"error" : "Request must be JSON"}, status = 400)
    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return json({"error": "Name and location are required"}, status=400)

    shelter = await Shelter.create(name=name, location=location)
    cache = caches.get("default")
    await cache.delete("shelter_list")
    
    return json({"message": "Shelter added successfully", "shelter": {
        "id": shelter.id, "name": shelter.name, "location": shelter.location
    }}, status=201)

@shelters_bp.route("/", methods=["GET"])
async def list_shelters(request):
    shelters = await Shelter.all().values("id", "name", "location")
    return json({"shelters": shelters}, status=200)

# READ - Tek Barýnak Detayý
@shelters_bp.route("/<shelter_id:int>", methods=["GET"])
async def get_shelter(request, shelter_id):
    shelter = await Shelter.get_or_none(id=shelter_id)
    if not shelter:
        return json({"error": "Shelter not found"}, status=404)

    return json({"shelter": {"id": shelter.id, "name": shelter.name, "location": shelter.location}}, status=200)

@shelters_bp.route("/update/<shelter_id:int>", methods=["PUT"])
async def update_shelter(request, shelter_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error" : "Authorization header is missing"}, status=401)
    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status = 401)
    if decoded.get("role") != "admin":
        return json({"error" :"Access denied"}, status=403)
    
    data = request.json
    shelter = await Shelter.get_or_none(id=shelter_id)

    if not shelter:
        return json({"error": "Shelter not found"}, status=404)

    shelter.name = data.get("name", shelter.name)
    shelter.location = data.get("location", shelter.location)
    await shelter.save()
    cache = caches.get("default")
    cache = caches.delete("shelter_list")

    return json({"message": "Shelter updated successfully", "shelter": {
        "id": shelter.id, "name": shelter.name, "location": shelter.location
    }}, status=200)

@shelters_bp.route("/delete/<shelter_id:int>", methods=["DELETE"])
async def delete_shelter(request, shelter_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error" : "Authorization header is missing"}, status = 401)
    
    decoded = decode_token(token)
    if  "error" in decoded:
        return json(decoded, status = 401)
    
    if decoded.get("role") != "admin":
        return json("Access denied", status = 403)
    shelter = await Shelter.get_or_none(id=shelter_id)

    if not shelter:
        return json({"error": "Shelter not found"}, status=404)
    
    cache = caches.get("default")
    cache = caches.delete("shelter_list")

    await shelter.delete()
    return json({"message": "Shelter deleted successfully"}, status=200)
