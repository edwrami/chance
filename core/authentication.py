from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class DocumentoBackend(BaseBackend):
    def authenticate(self, request, documento=None, password=None, username=None, **kwargs):
        # Aceptar tanto documento como username (para compatibilidad con admin estándar)
        identifier = documento or username
        if not identifier:
            return None
            
        try:
            user = User.objects.get(documento=identifier)
            if user.check_password(password) and user.activo:
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
