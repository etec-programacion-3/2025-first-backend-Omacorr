from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='sqlite://biblioteca.db',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()
