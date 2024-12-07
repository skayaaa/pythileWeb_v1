from tortoise.models import Model
from tortoise import fields

class Animal(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    species = fields.CharField(max_length=50)
    age = fields.IntField()
    shelter = fields.ForeignKeyField("models.Shelter", related_name="animals", on_delete=fields.CASCADE)
