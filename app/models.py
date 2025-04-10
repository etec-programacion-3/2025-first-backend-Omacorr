from tortoise import fields, models

class Product(models.Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    description = fields.TextField()

    class Meta:
        table = "products" 