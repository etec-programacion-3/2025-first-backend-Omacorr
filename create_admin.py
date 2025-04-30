"""
Script para crear un usuario administrador inicial en la base de datos.
Ejecutar con: python create_admin.py
"""
import asyncio
import sys
from tortoise import Tortoise

from models.usuario import Usuario

async def create_admin():
    """Crea un usuario administrador en la base de datos."""
    
    # Conexión a la base de datos
    await Tortoise.init(
        db_url="sqlite://biblioteca.db",
        modules={"models": ["models"]}
    )
    
    # Crear esquemas si no existen
    await Tortoise.generate_schemas()
    
    # Verificar si ya existe un administrador
    admin = await Usuario.filter(rol="admin").first()
    
    if admin:
        print(f"Ya existe un administrador: {admin.username}")
        return
    
    # Solicitar datos del administrador
    username = input("Nombre de usuario del administrador: ")
    email = input("Correo electrónico del administrador: ")
    password = input("Contraseña del administrador: ")
    nombre = input("Nombre completo del administrador: ")
    
    # Validaciones básicas
    if len(username) < 3:
        print("Error: El nombre de usuario debe tener al menos 3 caracteres")
        return
    
    if len(password) < 8:
        print("Error: La contraseña debe tener al menos 8 caracteres")
        return
    
    if "@" not in email:
        print("Error: El correo electrónico no es válido")
        return
    
    # Verificar si el username ya existe
    if await Usuario.filter(username=username).exists():
        print("Error: El nombre de usuario ya está en uso")
        return
    
    # Verificar si el email ya existe
    if await Usuario.filter(email=email).exists():
        print("Error: El correo electrónico ya está en uso")
        return
    
    try:
        # Crear el administrador
        admin = await Usuario.create_user(
            username=username,
            email=email,
            password=password,
            nombre=nombre,
            rol="admin"
        )
        
        print(f"Administrador creado exitosamente: {admin.username}")
    
    except Exception as e:
        print(f"Error al crear el administrador: {e}")
    
    # Cerrar conexión
    await Tortoise.close_connections()

if __name__ == "__main__":
    try:
        asyncio.run(create_admin())
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario")
        sys.exit(0)