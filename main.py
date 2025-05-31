from flask import Flask
from flask_cors import CORS
from app.routes import configure_routes
from app.database import initialize_database

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
initialize_database(app)

# Configurar las rutas
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)