from app import app, db, Libro
from datetime import datetime

def init_database():
    """Inicializa la base de datos y agrega datos de ejemplo"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar si ya hay datos
        if Libro.query.count() == 0:
            # Agregar libros de ejemplo
            libros_ejemplo = [
                Libro(
                    titulo="Cien años de soledad",
                    autor="Gabriel García Márquez",
                    isbn="9788437604947",
                    categoria="Ficción",
                    estado="disponible"
                ),
                Libro(
                    titulo="El nombre del viento",
                    autor="Patrick Rothfuss",
                    isbn="9788401337208",
                    categoria="Fantasía",
                    estado="disponible"
                ),
                Libro(
                    titulo="1984",
                    autor="George Orwell",
                    isbn="9788499890944",
                    categoria="Distopía",
                    estado="prestado"
                ),
                Libro(
                    titulo="El principito",
                    autor="Antoine de Saint-Exupéry",
                    isbn="9788498382083",
                    categoria="Infantil",
                    estado="disponible"
                ),
                Libro(
                    titulo="Don Quijote de la Mancha",
                    autor="Miguel de Cervantes",
                    isbn="9788467032802",
                    categoria="Clásico",
                    estado="disponible"
                )
            ]
            
            # Agregar todos los libros a la base de datos
            for libro in libros_ejemplo:
                db.session.add(libro)
            
            # Confirmar cambios
            db.session.commit()
            print(f"Base de datos inicializada con {len(libros_ejemplo)} libros de ejemplo")
        else:
            print("La base de datos ya contiene datos")

if __name__ == "__main__":
    init_database()