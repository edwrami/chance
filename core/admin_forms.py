from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate

class AdminAuthenticationForm(AuthenticationForm):
    """
    Formulario de login personalizado para el admin que usa documento en lugar de username
    """
    documento = forms.CharField(label="Documento", max_length=20)
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # Remover el campo username estándar
        if 'username' in self.fields:
            del self.fields['username']
    
    def clean(self):
        documento = self.cleaned_data.get('documento')
        password = self.cleaned_data.get('password')
        
        if documento is not None and password:
            self.user_cache = authenticate(
                self.request,
                documento=documento,
                password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data
