from tortoise.models import Model
from tortoise import fields

class Shelter(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    location = fields.CharField(max_length=255)
