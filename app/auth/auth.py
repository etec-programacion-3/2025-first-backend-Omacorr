from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from ..models.usuario import Usuario
from ..schemas.usuario import TokenData

# Configuración del token JWT
# En una aplicación real, estos valores deberían estar en variables de entorno
SECRET_KEY = "un_secreto_muy_seguro_que_deberia_estar_en_variables_de_entorno"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con los datos proporcionados y una fecha de expiración.
    
    Args:
        data: Datos a incluir en el token
        expires_delta: Tiempo de expiración (opcional)
        
    Returns:
        str: Token JWT generado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    """
    Obtiene el usuario actual a partir del token JWT.
    
    Args:
        token: Token JWT de autenticación
        
    Returns:
        Usuario: Objeto de usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    # Buscar el usuario en la base de datos
    user = await Usuario.get_or_none(username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user

def get_password_hash(password: str) -> str:
    """
    Obtiene el hash de una contraseña.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
    """
    from passlib.hash import bcrypt
    return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña
        
    Returns:
        bool: True si la contraseña es correcta, False en caso contrario
    """
    from passlib.hash import bcrypt
    return bcrypt.verify(plain_password, hashed_password)