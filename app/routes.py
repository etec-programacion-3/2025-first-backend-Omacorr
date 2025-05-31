from flask import Blueprint, request, jsonify
from app.models import Libro
from app.database import db

routes = Blueprint('routes', __name__)

@routes.route('/libros', methods=['GET'])
def obtener_libros():
    libros = Libro.query.all()
    return jsonify({
        'status': 'success',
        'data': [libro.to_dict() for libro in libros],
        'total': len(libros)
    }), 200

@routes.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    return jsonify({
        'status': 'success',
        'data': libro.to_dict()
    }), 200

@routes.route('/libros', methods=['POST'])
def crear_libro():
    data = request.get_json()
    campos_requeridos = ['titulo', 'autor', 'isbn', 'categoria']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'status': 'error',
                'message': f'El campo {campo} es requerido'
            }), 400

    if Libro.query.filter_by(isbn=data['isbn']).first():
        return jsonify({
            'status': 'error',
            'message': 'Ya existe un libro con este ISBN'
        }), 400

    nuevo_libro = Libro(
        titulo=data['titulo'],
        autor=data['autor'],
        isbn=data['isbn'],
        categoria=data['categoria'],
        estado=data.get('estado', 'disponible')
    )

    db.session.add(nuevo_libro)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Libro creado exitosamente',
        'data': nuevo_libro.to_dict()
    }), 201

@routes.route('/libros/<int:libro_id>', methods=['PUT'])
def actualizar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    data = request.get_json()

    if 'titulo' in data:
        libro.titulo = data['titulo']
    if 'autor' in data:
        libro.autor = data['autor']
    if 'isbn' in data:
        libro_existente = Libro.query.filter_by(isbn=data['isbn']).first()
        if libro_existente and libro_existente.id != libro_id:
            return jsonify({
                'status': 'error',
                'message': 'Ya existe un libro con este ISBN'
            }), 400
        libro.isbn = data['isbn']
    if 'categoria' in data:
        libro.categoria = data['categoria']
    if 'estado' in data:
        libro.estado = data['estado']

    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Libro actualizado exitosamente',
        'data': libro.to_dict()
    }), 200

@routes.route('/libros/<int:libro_id>', methods=['DELETE'])
def eliminar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    db.session.delete(libro)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Libro eliminado exitosamente'
    }), 200

@routes.route('/libros/buscar', methods=['GET'])
def buscar_libros():
    titulo = request.args.get('titulo', '')
    autor = request.args.get('autor', '')
    categoria = request.args.get('categoria', '')
    estado = request.args.get('estado', '')

    query = Libro.query

    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))
    if autor:
        query = query.filter(Libro.autor.ilike(f'%{autor}%'))
    if categoria:
        query = query.filter(Libro.categoria.ilike(f'%{categoria}%'))
    if estado:
        query = query.filter(Libro.estado.ilike(f'%{estado}%'))

    libros = query.all()

    return jsonify({
        'status': 'success',
        'data': [libro.to_dict() for libro in libros],
        'total': len(libros),
        'filtros': {
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'estado': estado
        }
    }), 200

def configure_routes(app):
    pass  # Aquí irán tus rutas