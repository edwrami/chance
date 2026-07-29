from django import forms
from .models import TwilioCredentials

class TwilioCredentialsForm(forms.ModelForm):
    class Meta:
        model = TwilioCredentials
        fields = ['account_sid', 'api_key_sid', 'api_key_secret', 'sms_number', 'whatsapp_number']
        widgets = {
            'api_key_secret': forms.PasswordInput(render_value=True),
        }
