# crear_admin_directo.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chancepro.settings')
django.setup()

from core.models import Usuario

def crear_admin():
    print("=== CREAR ADMINISTRADOR GENERAL ===")
    documento = input("Documento: ")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    direccion = input("Direccion: ")
    telefono = input("Telefono: ")
    telefono_familiar = input("Telefono familiar: ")
    password = input("Password: ")
    
    try:
        # Verificar si ya existe
        if Usuario.objects.filter(documento=documento).exists():
            print(f"El usuario {documento} ya existe")
            return
        
        usuario = Usuario(
            documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            direccion=direccion,
            telefono=telefono,
            telefono_familiar=telefono_familiar,
            is_staff=True,
            is_superuser=True,
            activo=True,
            rol='admin_general'
        )
        usuario.set_password(password)
        usuario.save()
        print(f"✅ Administrador {documento} creado exitosamente")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_admin()