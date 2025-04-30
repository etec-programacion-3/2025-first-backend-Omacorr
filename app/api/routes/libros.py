from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from tortoise.exceptions import DoesNotExist

from app.schemas.libro import Libro, LibroCreate, LibroUpdate
from app.db.models.libro import Libro as LibroModel

router = APIRouter()

@router.get("/", response_model=List[Libro])
async def get_libros():
    """
    Obtener todos los libros.
    
    Returns:
        List[Libro]: Lista de todos los libros en la base de datos.
    """
    return await Libro.from_queryset(LibroModel.all())

@router.get("/{libro_id}", response_model=Libro)
async def get_libro(libro_id: int):
    """
    Obtener un libro por su ID.
    
    Args:
        libro_id (int): ID del libro a obtener.
        
    Returns:
        Libro: Detalles del libro.
        
    Raises:
        HTTPException: Si el libro no existe.
    """
    try:
        libro = await LibroModel.get(id=libro_id)
        return libro
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )

@router.post("/", response_model=Libro, status_code=status.HTTP_201_CREATED)
async def create_libro(libro: LibroCreate):
    """
    Crear un nuevo libro.
    
    Args:
        libro (LibroCreate): Datos del libro a crear.
        
    Returns:
        Libro: Libro creado.
        
    Raises:
        HTTPException: Si ya existe un libro con el mismo ISBN.
    """
    # Verificar si ya existe un libro con el mismo ISBN
    if await LibroModel.filter(isbn=libro.isbn).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un libro con ISBN {libro.isbn}"
        )
    
    libro_obj = await LibroModel.create(**libro.dict())
    return libro_obj

@router.put("/{libro_id}", response_model=Libro)
async def update_libro(libro_id: int, libro: LibroUpdate):
    """
    Actualizar un libro existente.
    
    Args:
        libro_id (int): ID del libro a actualizar.
        libro (LibroUpdate): Datos a actualizar.
        
    Returns:
        Libro: Libro actualizado.
        
    Raises:
        HTTPException: Si el libro no existe.
    """
    try:
        libro_obj = await LibroModel.get(id=libro_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    
    # Filtrar solo los campos que no son None
    update_data = {k: v for k, v in libro.dict().items() if v is not None}
    
    # Si se intenta actualizar el ISBN, verificar que no exista otro libro con ese ISBN
    if "isbn" in update_data:
        existe = await LibroModel.filter(isbn=update_data["isbn"]).exclude(id=libro_id).exists()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otro libro con ISBN {update_data['isbn']}"
            )
    
    # Actualizar el libro
    await libro_obj.update_from_dict(update_data)
    await libro_obj.save()
    
    return libro_obj

@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_libro(libro_id: int):
    """
    Eliminar un libro.
    
    Args:
        libro_id (int): ID del libro a eliminar.
        
    Returns:
        None
        
    Raises:
        HTTPException: Si el libro no existe.
    """
    deleted_count = await LibroModel.filter(id=libro_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )

@router.get("/", response_model=List[Libro])
async def get_libros(
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    categoria: Optional[str] = None,
    estado: Optional[str] = None,
    ordenar_por: Optional[str] = "id",
    orden: Optional[str] = "asc",
    pagina: int = Query(1, ge=1),
    items_por_pagina: int = Query(10, ge=1, le=100)
):
    """
    Listar libros con opciones de filtrado, ordenamiento y paginación.
    
    Args:
        titulo (str, optional): Filtrar por título.
        autor (str, optional): Filtrar por autor.
        categoria (str, optional): Filtrar por categoría.
        estado (str, optional): Filtrar por estado.
        ordenar_por (str, optional): Campo por el cual ordenar.
        orden (str, optional): Dirección del ordenamiento (asc o desc).
        pagina (int): Número de página (inicia en 1).
        items_por_pagina (int): Cantidad de items por página.
        
    Returns:
        List[Libro]: Lista de libros filtrados, ordenados y paginados.
    """
    # Iniciar la consulta
    query = LibroModel.all()
    
    # Aplicar filtros si existen
    if titulo:
        query = query.filter(titulo__icontains=titulo)
    if autor:
        query = query.filter(autor__icontains=autor)
    if categoria:
        query = query.filter(categoria__icontains=categoria)
    if estado:
        query = query.filter(estado=estado)
    
    # Aplicar ordenamiento
    if orden.lower() == "desc":
        query = query.order_by(f"-{ordenar_por}")
    else:
        query = query.order_by(ordenar_por)
    
    # Aplicar paginación
    skip = (pagina - 1) * items_por_pagina
    query = query.offset(skip).limit(items_por_pagina)
    
    # Ejecutar la consulta
    return await query