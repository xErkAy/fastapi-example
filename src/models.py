from tortoise import fields

from core.models import BaseModel


class User(BaseModel):
    username = fields.CharField(max_length=30)
    password = fields.CharField(max_length=128)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.id}] {self.username}'

    def __repr__(self):
        return f'<User: [{self.id}] {self.username}>'
