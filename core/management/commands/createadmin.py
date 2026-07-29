import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create a super‑user admin using environment variables (useful for CI/CD)."

    def handle(self, *args, **options):
        # Expected env vars (provide defaults or raise if missing)
        documento = os.getenv("ADMIN_DOC")
        nombres = os.getenv("ADMIN_NOMBRES")
        apellidos = os.getenv("ADMIN_APELLIDOS")
        direccion = os.getenv("ADMIN_DIRECCION", "")
        telefono = os.getenv("ADMIN_TELEFONO", "")
        telefono_familiar = os.getenv("ADMIN_TELEFONO_FAMILIAR", "")
        password = os.getenv("ADMIN_PASSWORD")
        if not all([documento, nombres, apellidos, password]):
            self.stderr.write(self.style.ERROR("Missing required ADMIN_* environment variables."))
            return

        if User.objects.filter(documento=documento).exists():
            self.stdout.write(self.style.WARNING(f"User with documento {documento} already exists."))
            return

        user = User(
            documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            direccion=direccion,
            telefono=telefono,
            telefono_familiar=telefono_familiar,
            is_staff=True,
            is_superuser=True,
            activo=True,
            rol="admin_general",
        )
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"✅ Admin {documento} created successfully."))
