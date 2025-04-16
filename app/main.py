from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from app.models.libro import Libro
from app.schemas.libro import LibroIn, LibroOut

app = FastAPI()

@app.post("/libros", response_model=LibroOut)
async def crear_libro(libro: LibroIn):
    libro_db = await Libro.create(**libro.dict())
    return libro_db

@app.get("/libros", response_model=list[LibroOut])
async def listar_libros():
    libros = await Libro.all()
    return libros

@app.get("/libros/{id}", response_model=LibroOut)
async def obtener_libro(id: int):
    try:
        libro = await Libro.get(id=id)
        return libro
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/libros/{id}", response_model=LibroOut)
async def actualizar_libro(id: int, libro: LibroIn):
    try:
        libro_db = await Libro.get(id=id)
        for campo, valor in libro.dict().items():
            setattr(libro_db, campo, valor)
        await libro_db.save()
        return libro_db
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/libros/{id}")
async def eliminar_libro(id: int):
    try:
        libro_db = await Libro.get(id=id)
        await libro_db.delete()
        return {"message": "Libro eliminado exitosamente"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.get("/libros/buscar", response_model=list[LibroOut])
async def buscar_libros(titulo: str = None, autor: str = None, categoria: str = None):
    filtros = {}
    if titulo:
        filtros["titulo__icontains"] = titulo
    if autor:
        filtros["autor__icontains"] = autor
    if categoria:
        filtros["categoria__icontains"] = categoria
    libros = await Libro.filter(**filtros)
    return libros

# Conexión a la base de datos
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models.libro"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
