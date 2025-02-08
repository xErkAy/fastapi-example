from tortoise import Model, fields


class BaseModel(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True
