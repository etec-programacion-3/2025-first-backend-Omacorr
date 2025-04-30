from tortoise import fields
from tortoise.models import Model

class Usuario(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    apellido = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    rol = fields.CharField(max_length=50, default="usuario")  # usuario o admin
    activo = fields.BooleanField(default=True)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)
