from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class DocumentoBackend(BaseBackend):
    def authenticate(self, request, documento=None, password=None, **kwargs):
        try:
            user = User.objects.get(documento=documento)
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
