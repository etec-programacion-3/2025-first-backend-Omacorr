from tortoise import fields
from tortoise.models import Model

class Libro(Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    anio_publicacion = fields.IntField()
    isbn = fields.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.titulo

