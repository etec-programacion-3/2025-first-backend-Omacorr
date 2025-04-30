from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    """Esquema base para usuarios"""
    username: str
    email: EmailStr
    nombre: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'El nombre de usuario debe ser alfanumérico'
        return v

class UsuarioCreate(UsuarioBase):
    """Esquema para crear un usuario"""
    password: str
    
    @validator('password')
    def password_min_length(cls, v):
        assert len(v) >= 8, 'La contraseña debe tener al menos 8 caracteres'
        return v

class UsuarioUpdate(BaseModel):
    """Esquema para actualizar un usuario"""
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    
    @validator('password')
    def password_min_length(cls, v):
        if v is not None:
            assert len(v) >= 8, 'La contraseña debe tener al menos 8 caracteres'
        return v

class UsuarioAdminUpdate(UsuarioUpdate):
    """Esquema para que un administrador actualice un usuario"""
    rol: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioOut(UsuarioBase):
    """Esquema para la salida de datos de un usuario"""
    id: int
    rol: str
    activo: bool
    fecha_registro: datetime
    
    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    """Esquema para login de usuario"""
    username: str
    password: str

class Token(BaseModel):
    """Esquema para el token de autenticación"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Datos contenidos en el token"""
    username: Optional[str] = None