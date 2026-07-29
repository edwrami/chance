import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chancepro.settings')
django.setup()

from django.contrib.auth import authenticate
from core.models import Usuario

# Obtener el usuario
try:
    usuario = Usuario.objects.get(documento='9975334')
    print(f"Usuario encontrado: {usuario.documento} - {usuario.nombres} {usuario.apellidos}")
    print(f"Is staff: {usuario.is_staff}")
    print(f"Is superuser: {usuario.is_superuser}")
    print(f"Activo: {usuario.activo}")
    print(f"Rol: {usuario.rol}")
    
    # Probar autenticación con documento
    user = authenticate(documento='9975334', password='edwrami0483')
    print(f"Autenticación con documento: {user}")
    
    # Probar autenticación con username
    user2 = authenticate(username='9975334', password='edwrami0483')
    print(f"Autenticación con username: {user2}")
    
    # Probar verificación de contraseña
    print(f"Verificación de contraseña: {usuario.check_password('edwrami0483')}")
    
except Usuario.DoesNotExist:
    print("Usuario no encontrado")
