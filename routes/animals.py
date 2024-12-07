from sanic import Blueprint
from models.animals import Animal
from models.shelters import Shelter
from sanic.response import json

animals_bp = Blueprint("animals", url_prefix="/animals")

@animals_bp.route("/add", methods=["POST"])
async def add_animal(request):
    data = request.json
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
    return json({"message": "Animal added successfully", "animal": {
        "id": animal.id, "name": animal.name, "species": animal.species, "age": animal.age,
        "shelter_id": animal.shelter_id
    }}, status=201)

@animals_bp.route("/", methods=["GET"])
async def list_animals(request):
    animals = await Animal.all().values("id", "name", "species", "age", "shelter_id")
    return json({"animals": animals}, status=200)

@animals_bp.route("/<animal_id:int>", methods=["GET"])
async def get_animal(request, animal_id):
    animal = await Animal.get_or_none(id=animal_id)
    if not animal:
        return json({"error": "Animal not found"}, status=404)

    return json({"animal": {"id": animal.id, "name": animal.name, "species": animal.species, "age": animal.age, "shelter_id": animal.shelter_id}}, status=200)

@animals_bp.route("/update/<animal_id:int>", methods=["PUT"])
async def update_animal(request, animal_id):
    data = request.json
    animal = await Animal.get_or_none(id=animal_id)

    if not animal:
        return json({"error": "Animal not found"}, status=404)

    animal.name = data.get("name", animal.name)
    animal.species = data.get("species", animal.species)
    animal.age = data.get("age", animal.age)
    await animal.save()

    return json({"message": "Animal updated successfully", "animal": {
        "id": animal.id, "name": animal.name, "species": animal.species, "age": animal.age,
        "shelter_id": animal.shelter_id
    }}, status=200)

@animals_bp.route("/delete/<animal_id:int>", methods=["DELETE"])
async def delete_animal(request, animal_id):
    animal = await Animal.get_or_none(id=animal_id)

    if not animal:
        return json({"error": "Animal not found"}, status=404)

    await animal.delete()
    return json({"message": "Animal deleted successfully"}, status=200)
