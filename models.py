from tortoise import fields
from tortoise.models import Model

class User(Model):
    discord_id = fields.BigIntField(pk = True)
    db_points = fields.IntField(default = 0)
    correct_answers = fields.IntField(default = 0)
    total_quizes = fields.IntField(default = 0)
    
    class Meta:
        table = "users"