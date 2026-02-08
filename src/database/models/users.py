from tortoise.fields import IntField, CharField
from tortoise.models import Model


class Users(Model):
    id = IntField(pk=True)
    user_id = CharField(max_length=50, unique=True)
    language = CharField(max_length=5)

    class Meta:
        table = "users"

    def __repr__(self):
        return "Users(user_id={}, language={})".format(self.user_id, self.language)