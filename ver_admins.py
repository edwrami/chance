import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chancepro.settings')
django.setup()

from core.models import Usuario

print("=== USUARIOS ADMINISTRADORES ===")
admins = Usuario.objects.filter(is_superuser=True)

if admins.exists():
    for admin in admins:
        print(f"\nDocumento: {admin.documento}")
        print(f"Nombres: {admin.nombres} {admin.apellidos}")
        print(f"Email: {admin.email}")
        print(f"Teléfono: {admin.telefono}")
        print(f"Activo: {admin.activo}")
        print(f"Rol: {admin.rol}")
        print(f"Is staff: {admin.is_staff}")
        print(f"Is superuser: {admin.is_superuser}")
        print(f"Fecha creación: {admin.created_at}")
else:
    print("No hay usuarios administradores creados")
