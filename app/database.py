from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

def initialize_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea todas las tablas en la base de datos

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='disponible')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'categoria': self.categoria,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }