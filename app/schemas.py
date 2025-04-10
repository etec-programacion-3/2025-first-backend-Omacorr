from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)

class ProductCreateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True) 