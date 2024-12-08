from sanic import Blueprint
from models.animals import Animal
from models.shelters import Shelter
from sanic.response import json
from aiocache import cached , caches
from utils.auth_utils import decode_token

animals_bp = Blueprint("animals", url_prefix="/animals")
@cached(ttl=60, key = "animal_list")
async def get_animals_list():
    animals = await Animal.all().values("id","name","species","age","shelter_id")
    return animals
    

@animals_bp.route("/add", methods=["POST"])
async def add_animal(request):
    
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error" :"Authorization header is missing"}, status = 401)
    
    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded, status = 401)
    
    if decoded.get("role") != "admin":
        return json({"error" : "Access denied"}, status = 403)
    
    data = request.json
    if not data:
        return json({"error": "Request body must be JSON"}, status = 400)
    name = data.get("name")
    species = data.get("species")
    age = data.get("age")
    shelter_id = data.get("shelter_id")
    

    if not name or not species or not age or not shelter_id:
        return json({"error": "Name, species, age, and shelter_id are required"}, status=400)

    shelter = await Shelter.get_or_none(id=shelter_id)
    if not shelter:
        return json({"error": "Shelter not found"}, status=404)

    animal = await Animal.create(name=name, species=species, age=age, shelter=shelter)
    
    cache = caches.get("default")
    await cache.delete("animals_list")
    
    return json({"message": "Animal added successfully", "animal": {
        "id": animal.id, "name": animal.name, "species": animal.species, "age": animal.age,
        "shelter_id": animal.shelter_id
    }}, status=201)

@animals_bp.route("/", methods=["GET"])
async def list_animals(request):
    animals = await get_animals_list()
    return json({"animals": animals}, status=200)

@animals_bp.route("/<animal_id:int>", methods=["GET"])
async def get_animal(request, animal_id):
    animal = await Animal.get_or_none(id=animal_id)
    if not animal:
        return json({"error": "Animal not found"}, status=404)

    return json({"animal": {"id": animal.id, "name": animal.name, "species": animal.species, "age": animal.age, "shelter_id": animal.shelter_id}}, status=200)

@animals_bp.route("/update/<animal_id:int>", methods=["PUT"])
async def update_animal(request, animal_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error" : "Aurhorization header is missing"}, status = 401)
    
    decoded = decode_token(token)
    if "error" in token:
        return json(decoded, status=401)
    if decoded.get("role") != "admim":
        return json({"error" : "Access denied"}, status = 403)
    data = request.json
    animal = await Animal.get_or_none(id=animal_id)

    if not animal:
        return json({"error": "Animal not found"}, status=404)

    animal.name = data.get("name", animal.name)
    animal.species = data.get("species", animal.species)
    animal.age = data.get("age", animal.age)
    await animal.save()
    cache = caches.get("default")
    await cache.delete("animals_list")
    

    return json({"message": "Animal updated successfully", "animal": {
        "id": animal.id, "name": animal.name, "species": animal.species, "age": animal.age,
        "shelter_id": animal.shelter_id
    }}, status=200)

@animals_bp.route("/delete/<animal_id:int>", methods=["DELETE"])
async def delete_animal(request, animal_id):
    animal = await Animal.get_or_none(id=animal_id)
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return json({"error" : "Authorization header is missing"}, status = 401)
    decoded = decode_token(token)
    if "error" in decoded:
        return json(decoded , status = 401)
    if decoded.get("role") != "admin":
        return json({"error" : "Animal not found"}, status = 404)

    if not animal:
        return json({"error": "Animal not found"}, status=404)

    await animal.delete()
    
    cache = caches.get("default")
    await cache.delete("animals_list")
    return json({"message": "Animal deleted successfully"}, status=200)
