from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def _create_user(self, documento, nombres, apellidos, direccion, telefono, telefono_familiar, password, **extra_fields):
        if not documento:
            raise ValueError('El documento es obligatorio')
        if not nombres:
            raise ValueError('Los nombres son obligatorios')
        if not apellidos:
            raise ValueError('Los apellidos son obligatorios')
        
        user = self.model(
            documento=documento,
            nombres=nombres,
            apellidos=apellidos,
            direccion=direccion,
            telefono=telefono,
            telefono_familiar=telefono_familiar,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, documento, nombres, apellidos, direccion, telefono, telefono_familiar, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(documento, nombres, apellidos, direccion, telefono, telefono_familiar, password, **extra_fields)

    def create_superuser(self, documento, nombres, apellidos, direccion, telefono, telefono_familiar, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('activo', True)
        extra_fields.setdefault('rol', 'admin_general')
        return self._create_user(documento, nombres, apellidos, direccion, telefono, telefono_familiar, password, **extra_fields)