from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from ..models.usuario import Usuario
from ..schemas.usuario import Token, UsuarioCreate, UsuarioOut
from ..auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["autenticación"]
)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para obtener un token de acceso mediante login.
    
    Args:
        form_data: Formulario con username y password
        
    Returns:
        Token: Token de acceso JWT
        
    Raises:
        HTTPException: Si las credenciales son incorrectas
    """
    # Buscar el usuario
    user = await Usuario.get_or_none(username=form_data.username)
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar si el usuario está activo
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear el token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UsuarioCreate):
    """
    Endpoint para registrar un nuevo usuario.
    
    Args:
        user_data: Datos del usuario a registrar
        
    Returns:
        UsuarioOut: Datos del usuario registrado
        
    Raises:
        HTTPException: Si el username o email ya existen
    """
    # Verificar si el username ya existe
    if await Usuario.filter(username=user_data.username).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Verificar si el email ya existe
    if await Usuario.filter(email=user_data.email).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está en uso"
        )
    
    # Crear el usuario
    user = await Usuario.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        nombre=user_data.nombre
    )
    
    return user