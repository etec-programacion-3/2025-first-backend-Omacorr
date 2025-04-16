TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models.libro"],  # Aerich se usa para migraciones
            "default_connection": "default",
        },
    },
}
