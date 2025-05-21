from fastapi import APIRouter, HTTPException
from app.schemas.usuario import UsuarioCreate, UsuarioLogin
from db.models.usuario import Usuario
from app.core.security import hash_password, verify_password

router = APIRouter()

@router.post("/register")
async def register(user: UsuarioCreate):
    existing_user = await Usuario.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_pw = hash_password(user.password)
    new_user = await Usuario.create(nombre=user.nombre, email=user.email, password=hashed_pw)
    return {"message": "Usuario creado", "usuario": new_user.email}


@router.post("/login")
async def login(user: UsuarioLogin):
    db_user = await Usuario.get_or_none(email=user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"message": f"Bienvenido, {db_user.nombre}"}
