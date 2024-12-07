from sanic import Blueprint, response
from models.shelters import Shelter
from sanic.response import json

shelters_bp = Blueprint("shelters", url_prefix="/shelters")

@shelters_bp.route("/add", methods=["POST"])
async def add_shelter(request):
    data = request.json
    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return json({"error": "Name and location are required"}, status=400)

    shelter = await Shelter.create(name=name, location=location)
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
    data = request.json
    shelter = await Shelter.get_or_none(id=shelter_id)

    if not shelter:
        return json({"error": "Shelter not found"}, status=404)

    shelter.name = data.get("name", shelter.name)
    shelter.location = data.get("location", shelter.location)
    await shelter.save()

    return json({"message": "Shelter updated successfully", "shelter": {
        "id": shelter.id, "name": shelter.name, "location": shelter.location
    }}, status=200)

@shelters_bp.route("/delete/<shelter_id:int>", methods=["DELETE"])
async def delete_shelter(request, shelter_id):
    shelter = await Shelter.get_or_none(id=shelter_id)

    if not shelter:
        return json({"error": "Shelter not found"}, status=404)

    await shelter.delete()
    return json({"message": "Shelter deleted successfully"}, status=200)
