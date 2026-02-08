from tortoise.fields import IntField, CharField
from tortoise.models import Model


class Groups(Model):
    id = IntField(pk=True)
    group_id = CharField(max_length=50, unique=True)

    class Meta:
        table = "groups"

    def __repr__(self):
        return "Group(group_id={}, joined_at={})".format(self.user_id, self.joined_at)