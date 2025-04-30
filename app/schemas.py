from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str
