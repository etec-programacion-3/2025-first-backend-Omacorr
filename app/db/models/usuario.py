from tortoise import fields, models
from passlib.hash import bcrypt

class Usuario(models.Model):
    """
    Modelo de Usuario para la aplicación de biblioteca.
    
    Atributos:
        id: Identificador único del usuario
        username: Nombre de usuario, único en el sistema
        email: Correo electrónico del usuario, único en el sistema
        hashed_password: Contraseña encriptada
        nombre: Nombre completo del usuario
        rol: Rol del usuario (admin, bibliotecario, usuario)
        activo: Indica si el usuario está activo en el sistema
        fecha_registro: Fecha de registro del usuario
    """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    nombre = fields.CharField(max_length=100, null=True)
    rol = fields.CharField(max_length=20, default="usuario")  # admin, bibliotecario, usuario
    activo = fields.BooleanField(default=True)
    fecha_registro = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "usuarios"
    
    def __str__(self):
        return f"{self.username} ({self.rol})"
    
    def verify_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        
        Args:
            password: Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario
        """
        return bcrypt.verify(password, self.hashed_password)
    
    @classmethod
    async def create_user(cls, username: str, email: str, password: str, nombre: str = None, rol: str = "usuario"):
        """
        Crea un nuevo usuario con la contraseña encriptada.
        
        Args:
            username: Nombre de usuario único
            email: Correo electrónico único
            password: Contraseña en texto plano (será encriptada)
            nombre: Nombre completo del usuario (opcional)
            rol: Rol del usuario (por defecto "usuario")
            
        Returns:
            Usuario: El objeto usuario creado
        """
        # Encriptar la contraseña
        hashed_password = bcrypt.hash(password)
        
        # Crear el usuario
        return await cls.create(
            username=username,
            email=email,
            hashed_password=hashed_password,
            nombre=nombre,
            rol=rol
        )