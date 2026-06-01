from django.core.management.base import BaseCommand
from core.models import Usuario
from getpass import getpass

class Command(BaseCommand):
    help = 'Crea un administrador general personalizado'

    def handle(self, *args, **options):
        self.stdout.write('=== CREAR ADMINISTRADOR GENERAL ===')
        
        # Solicitar datos
        documento = input('Documento: ')
        nombres = input('Nombres: ')
        apellidos = input('Apellidos: ')
        direccion = input('Direccion: ')
        telefono = input('Telefono: ')
        telefono_familiar = input('Telefono familiar: ')
        
        # Solicitar contraseña
        password = getpass('Password: ')
        password2 = getpass('Password (again): ')
        
        if password != password2:
            self.stdout.write(self.style.ERROR('Las contraseñas no coinciden'))
            return
        
        # Crear usuario
        try:
            usuario = Usuario.objects.create_superuser(
                documento=documento,
                nombres=nombres,
                apellidos=apellidos,
                direccion=direccion,
                telefono=telefono,
                telefono_familiar=telefono_familiar,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Administrador {documento} creado exitosamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            