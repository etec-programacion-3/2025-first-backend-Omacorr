from tortoise.expressions import Q
from app.models import Product

async def get_product(product_id: int):
    return await Product.get_or_none(id=product_id)

async def get_products(skip: int = 0, limit: int = 100):
    return await Product.all().offset(skip).limit(limit)

async def create_product(product: dict):
    return await Product.create(**product)

async def update_product(product_id: int, product: dict):
    await Product.filter(id=product_id).update(**product)
    return await get_product(product_id)

async def delete_product(product_id: int):
    deleted_count = await Product.filter(id=product_id).delete()
    return deleted_count > 0 