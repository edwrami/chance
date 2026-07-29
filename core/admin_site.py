# core/admin_site.py
from django.contrib.admin import AdminSite
from django.contrib.auth.views import LoginView
from django.urls import path
from django.shortcuts import redirect
from core.admin_forms import AdminAuthenticationForm

class DinnerProAdminSite(AdminSite):
    site_header = 'DinnerPro Administración'
    site_title = 'DinnerPro'
    index_title = 'Panel de Control'
    site_url = None
    login_form = AdminAuthenticationForm
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('login/', self.admin_view(LoginView.as_view(
                template_name='admin/login.html',
                authentication_form=self.login_form
            )), name='login'),
        ]
        return custom_urls + urls

# Crear instancia personalizada
admin_site = DinnerProAdminSite(name='chancepro_admin')
