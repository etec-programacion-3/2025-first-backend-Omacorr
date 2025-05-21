from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Biblioteca API"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Configuración de la base de datos
    DB_URL: str = "sqlite://./biblioteca.db"
    
    class Config:
        env_file = ".env"

settings = Settings()