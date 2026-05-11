from tortoise import fields
from tortoise.models import Model

class User(Model):
    discord_id = fields.BigIntField(pk = True)
    callsign = fields.CharField(max_length=10, null=True, default=None)
    bio = fields.CharField(max_length=200, null=True, default=None)
    db_points = fields.IntField(default = 0)
    correct_answers = fields.IntField(default = 0)
    total_quizzes = fields.IntField(default = 0)
    
    class Meta:
        table = "users"