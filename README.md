# Proyecto Backend - Sistema de Gestión de Biblioteca

## Información del Alumno
- Nombre y Apellido: Omar Correa
- Curso: 5to Año
- Especialidad: Informática

## Configuración del Repositorio
- La rama `main` debe estar protegida
- No se permiten push directos a `main`
- Todos los cambios deben realizarse a través de Pull Requests
- Los Pull Requests deben ser aprobados antes de ser mergeados

## Descripción
Este proyecto consiste en desarrollar un sistema backend para la gestión de una biblioteca escolar. El desarrollo se realizará en tres fases incrementales.

## Fase 1: Gestión de Libros

### Modelo de Datos
```python
class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='disponible')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
```

### Endpoints
```
GET    /libros           # Listar todos los libros
GET    /libros/{id}      # Obtener un libro específico
POST   /libros           # Crear un nuevo libro
PUT    /libros/{id}      # Actualizar un libro
DELETE /libros/{id}      # Eliminar un libro
GET    /libros/buscar    # Buscar libros (parámetros: titulo, autor, categoria)
```

### Milestones Fase 1
1. Configuración Inicial
   - [ ] Configurar el proyecto base
   - [ ] Implementar la conexión a la base de datos
   - [ ] Crear el modelo de libros

2. CRUD Básico
   - [ ] Implementar endpoints para libros
   - [ ] Implementar validación de datos
   - [ ] Documentar los endpoints

3. Búsqueda y Filtrado
   - [ ] Implementar búsqueda por título
   - [ ] Implementar filtrado por categoría
   - [ ] Implementar ordenamiento
   - [ ] Implementar paginación

### Pruebas de la API
- Se recomienda utilizar el archivo `tests/test_api.py` para probar los endpoints.
- Asegúrate de que la base de datos esté inicializada antes de ejecutar las pruebas.