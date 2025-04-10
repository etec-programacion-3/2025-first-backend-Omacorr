from fastapi import APIRouter, HTTPException
from typing import List

from app import crud
from app.schemas import ProductSchema, ProductCreateSchema

router = APIRouter()
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
product_create_schema = ProductCreateSchema()

@router.get("/", response_model=List[dict])
async def read_products(skip: int = 0, limit: int = 100):
    products = await crud.get_products(skip=skip, limit=limit)
    return products_schema.dump(products)

@router.get("/{product_id}", response_model=dict)
async def read_product(product_id: int):
    db_product = await crud.get_product(product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_schema.dump(db_product)

@router.post("/", response_model=dict)
async def create_product(product_data: dict):
    # Validate and deserialize input data
    data = product_create_schema.load(product_data)
    product = await crud.create_product(data)
    return product_schema.dump(product)

@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: int, product_data: dict):
    # Validate and deserialize input data
    data = product_create_schema.load(product_data)
    db_product = await crud.update_product(product_id=product_id, product=data)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_schema.dump(db_product)

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    success = await crud.delete_product(product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"} 