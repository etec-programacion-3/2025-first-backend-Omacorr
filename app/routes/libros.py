from fastapi import APIRouter, HTTPException
from models.libro import LibroCreate, LibroUpdate, Libro
from db.models.libro import Libro as LibroModel

router = APIRouter(prefix="/libros", tags=["Libros"])

# Crear un libro
@router.post("/", response_model=Libro)
async def crear_libro(libro: LibroCreate):
    libro_obj = await LibroModel.create(**libro.dict())
    return await Libro.from_tortoise_orm(libro_obj)

# Obtener todos los libros
@router.get("/", response_model=list[Libro])
async def listar_libros():
    libros = await LibroModel.all()
    return [await Libro.from_tortoise_orm(libro) for libro in libros]

# Obtener un libro por ID
@router.get("/{libro_id}", response_model=Libro)
async def obtener_libro(libro_id: int):
    libro = await LibroModel.get_or_none(id=libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return await Libro.from_tortoise_orm(libro)

# Actualizar un libro
@router.put("/{libro_id}", response_model=Libro)
async def actualizar_libro(libro_id: int, libro_data: LibroUpdate):
    libro = await LibroModel.get_or_none(id=libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    libro_data_dict = libro_data.dict(exclude_unset=True)
    for campo, valor in libro_data_dict.items():
        setattr(libro, campo, valor)
    
    await libro.save()
    return await Libro.from_tortoise_orm(libro)

# Eliminar un libro
@router.delete("/{libro_id}")
async def eliminar_libro(libro_id: int):
    libro = await LibroModel.get_or_none(id=libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    await libro.delete()
    return {"detalle": "Libro eliminado"}
