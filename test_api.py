import requests
import json

# URL base de la API
BASE_URL = "http://localhost:5000"

def test_api():
    """Prueba todos los endpoints de la API"""
    
    print("=== PRUEBAS DE LA API DE GESTIÓN DE LIBROS ===\n")
    
    # 1. Obtener documentación
    print("1. Obteniendo documentación de la API...")
    try:
        response = requests.get(f"{BASE_URL}/api/docs")
        if response.status_code == 200:
            print("✅ Documentación obtenida exitosamente")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Listar todos los libros
    print("2. Listando todos los libros...")
    try:
        response = requests.get(f"{BASE_URL}/libros")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Se encontraron {data['total']} libros")
            for libro in data['data']:
                print(f"   - {libro['titulo']} por {libro['autor']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Crear un nuevo libro
    print("3. Creando un nuevo libro...")
    nuevo_libro = {
        "titulo": "El Hobbit",
        "autor": "J.R.R. Tolkien",
        "isbn": "9788445077023",
        "categoria": "Fantasía",
        "estado": "disponible"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/libros", json=nuevo_libro)
        if response.status_code == 201:
            data = response.json()
            libro_id = data['data']['id']
            print(f"✅ Libro creado exitosamente con ID: {libro_id}")
            print(f"   Título: {data['data']['titulo']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.json()}")
            libro_id = None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        libro_id = None
    
    print("\n" + "="*50 + "\n")
    
    # 4. Obtener un libro específico
    if libro_id:
        print(f"4. Obteniendo libro con ID {libro_id}...")
        try:
            response = requests.get(f"{BASE_URL}/libros/{libro_id}")
            if response.status_code == 200:
                data = response.json()
                print("✅ Libro obtenido exitosamente:")
                print(json.dumps(data['data'], indent=2, ensure_ascii=False))
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Actualizar el libro
    if libro_id:
        print(f"5. Actualizando libro con ID {libro_id}...")
        actualizacion = {
            "estado": "prestado"
        }
        
        try:
            response = requests.put(f"{BASE_URL}/libros/{libro_id}", json=actualizacion)
            if response.status_code == 200:
                data = response.json()
                print("✅ Libro actualizado exitosamente")
                print(f"   Nuevo estado: {data['data']['estado']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 6. Buscar libros
    print("6. Buscando libros por categoría 'Fantasía'...")
    try:
        response = requests.get(f"{BASE_URL}/libros/buscar", params={"categoria": "Fantasía"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Búsqueda exitosa: {data['total']} libros encontrados")
            for libro in data['data']:
                print(f"   - {libro['titulo']} por {libro['autor']} ({libro['estado']})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 7. Buscar por título
    print("7. Buscando libros por título que contenga 'Quijote'...")
    try:
        response = requests.get(f"{BASE_URL}/libros/buscar", params={"titulo": "Quijote"})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Búsqueda exitosa: {data['total']} libros encontrados")
            for libro in data['data']:
                print(f"   - {libro['titulo']} por {libro['autor']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 8. Eliminar libro (opcional - descomenta si quieres probarlo)
    # if libro_id:
    #     print(f"8. Eliminando libro con ID {libro_id}...")
    #     try:
    #         response = requests.delete(f"{BASE_URL}/libros/{libro_id}")
    #         if response.status_code == 200:
    #             print("✅ Libro eliminado exitosamente")
    #         else:
    #             print(f"❌ Error: {response.status_code}")
    #     except Exception as e:
    #         print(f"❌ Error de conexión: {e}")
    
    print("=== PRUEBAS COMPLETADAS ===")

if __name__ == "__main__":
    test_api()