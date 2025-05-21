from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str = Field(..., description="ISBN único del libro")
    categoria: str
    estado: str = "disponible"

class LibroCreate(LibroBase):
    pass

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None

class LibroInDB(LibroBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True  # Equivalente a orm_mode en Pydantic v1

class Libro(LibroInDB):
    pass