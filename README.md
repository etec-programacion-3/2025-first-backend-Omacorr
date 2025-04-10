# Product API with FastAPI

A RESTful API for managing products built with FastAPI, SQLAlchemy, and SQLite.

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