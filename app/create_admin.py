from app.core.security import hash_password
from db.models.usuario import Usuario  # o desde donde tengas definido tu modelo
from tortoise.transactions import in_transaction

async def crear_admin():
    hashed_pw = hash_password("admin123")  # reemplazá por tu contraseña real
    async with in_transaction():
        await Usuario.create(nombre="admin", email="admin@example.com", password=hashed_pw)

# Para ejecutarlo directamente:
import asyncio
asyncio.run(crear_admin())
