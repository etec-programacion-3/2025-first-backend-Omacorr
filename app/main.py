from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from routes import libros, usuarios, prestamos, notificaciones, auth

app = FastAPI(
    title="Biblioteca API",
    description="API para gestión de biblioteca",
    version="0.3.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas
app.include_router(auth.router)
app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)
app.include_router(notificaciones.router)

# Configurar Tortoise ORM
register_tortoise(
    app,
    db_url="sqlite://biblioteca.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Ruta de inicio
@app.get("/", tags=["Inicio"])
async def root():
    return {
        "mensaje": "Bienvenido a la API de Biblioteca",
        "documentación": "/docs",
        "versión": "0.3.0"
    }

# Ejecutar con: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from app.routes import auth
app.include_router(auth.router, prefix="/auth")

