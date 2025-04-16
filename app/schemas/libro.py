from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LibroIn(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str

class LibroOut(LibroIn):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True
