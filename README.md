# Product API with FastAPI

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tortoise ORM](https://img.shields.io/badge/Tortoise_ORM-FF6F00?style=for-the-badge)](https://tortoise-orm.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Marshmallow](https://img.shields.io/badge/Marshmallow-FF6F00?style=for-the-badge)](https://marshmallow.readthedocs.io/)

A RESTful API for managing products built with modern Python technologies.

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Tortoise ORM**: Easy-to-use asyncio ORM inspired by Django
- **SQLite**: Lightweight, file-based database
- **Marshmallow**: Object serialization/deserialization library
- **Uvicorn**: ASGI server for running FastAPI applications
- **Python 3.13**: Latest Python version with improved performance and features

## Features

- Full CRUD operations for products
- Async database operations
- Request/response validation
- Automatic API documentation
- CORS support
- SQLite database with Tortoise ORM
- Comprehensive error handling

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python -m app.init_db
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

- GET /api/products - Get all products
- GET /api/products/{id} - Get a specific product
- POST /api/products - Create a new product
- PUT /api/products/{id} - Update a product
- DELETE /api/products/{id} - Delete a product

## Example Requests

See the `requests.http` file for example API requests that you can use with VS Code's REST Client or similar tools.

## Development

This project uses:
- Conventional Commits for commit messages
- SQLite for development database
- Tortoise ORM for database operations
- Marshmallow for data validation
- FastAPI for the API framework