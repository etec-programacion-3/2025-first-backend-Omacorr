from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioOut, UsuarioUpdate, UsuarioAdminUpdate
from ..auth.auth import get_current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/me", response_model=UsuarioOut)
async def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """
    Obtiene información del usuario actual autenticado.
    
    Args:
        current_user: Usuario autenticado (obtenido del token)
        
    Returns:
        UsuarioOut: Datos del usuario
    """
    return current_user

@router.put("/me", response_model=UsuarioOut)
async def update_user_me(
    user_update: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza información del usuario actual.
    
    Args:
        user_update: Datos a actualizar
        current_user: Usuario autenticado (obtenido del token)
        
    Returns:
        UsuarioOut: Datos actualizados del usuario
    """
    # Actualizar email si se proporciona y es diferente
    if user_update.email and user_update.email != current_user.email:
        # Verificar si el email ya está en uso
        if await Usuario.filter(email=user_update.email).exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está en uso"
            )
        current_user.email = user_update.email
    
    # Actualizar nombre si se proporciona
    if user_update.nombre is not None:
        current_user.nombre = user_update.nombre
    
    # Actualizar contraseña si se proporciona
    if user_update.password:
        from ..auth.auth import get_password_hash
        current_user.hashed_password = get_password_hash(user_update.password)
    
    # Guardar cambios
    await current_user.save()
    
    return current_user

@router.get("/", response_model=List[UsuarioOut])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene lista de usuarios (solo para administradores).
    
    Args:
        skip: Número de registros a omitir (para paginación)
        limit: Número máximo de registros a devolver
        current_user: Usuario autenticado (obtenido del token)
        
    Returns:
        List[UsuarioOut]: Lista de usuarios
        
    Raises:
        HTTPException: Si el usuario no es administrador
    """
    # Verificar si el usuario es administrador
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    # Obtener usuarios con paginación
    users = await Usuario.all().offset(skip).limit(limit)
    
    return users

@router.get("/{user_id}", response_model=UsuarioOut)
async def read_user(
    user_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene información de un usuario específico.
    
    Args:
        user_id: ID del usuario
        current_user: Usuario autenticado (obtenido del token)
        
    Returns:
        UsuarioOut: Datos del usuario
        
    Raises:
        HTTPException: Si el usuario no tiene permiso o el usuario no existe
    """
    # Verificar permisos
    if current_user.id != user_id and current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
    # Obtener usuario
    user = await Usuario.get_or_none(id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user

@router.put("/{user_id}", response_model=UsuarioOut)
async def update_user(
    user_id: int,
    user_update: UsuarioAdminUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza información de un usuario (solo para administradores).
    
    Args:
        user_id: ID del usuario a actualizar
        user_update: Datos a actualizar
        current_user: Usuario autenticado (obtenido del token)
        
    Returns:
        UsuarioOut: Datos actualizados del usuario
        
    Raises:
        HTTPException: Si el usuario no tiene permiso o el usuario no existe
    """
    # Verificar si el usuario es administrador
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    # Obtener usuario
    user = await Usuario.get_or_none(id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar email si se proporciona y es diferente
    if user_update.email and user_update.email != user.email:
        # Verificar si el email ya está en uso
        if await Usuario.filter(email=user_update.email).exists():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está en uso"
            )
        user.email = user_update.email
    
    # Actualizar otros campos si se proporcionan
    if user_update.nombre is not None:
        user.nombre = user_update.nombre
    
    if user_update.password:
        from ..auth.auth import get_password_hash
        user.hashed_password = get_password_hash(user_update.password)
    
    if user_update.rol is not None:
        # Validar que el rol sea válido
        if user_update.rol not in ["admin", "bibliotecario", "usuario"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rol no válido. Debe ser 'admin', 'bibliotecario' o 'usuario'"
            )
        user.rol = user_update.rol
    
    if user_update.activo is not None:
        user.activo = user_update.activo
    
    # Guardar cambios
    await user.save()
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina un usuario (solo para administradores).
    
    Args:
        user_id: ID del usuario a eliminar
        current_user: Usuario autenticado (obtenido del token)
        
    Raises:
        HTTPException: Si el usuario no tiene permiso o el usuario no existe
    """
    # Verificar si el usuario es administrador
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    # Verificar que no se esté eliminando a sí mismo
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario"
        )
    
    # Obtener usuario
    user = await Usuario.get_or_none(id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Eliminar usuario
    await user.delete()