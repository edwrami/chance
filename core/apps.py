from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'ChancePro'
    
    def ready(self):
        """
        Personalizar el admin cuando la app esté lista
        """
        from django.contrib import admin
        admin.site.site_header = 'ChancePro Administración'
        admin.site.site_title = 'ChancePro'
        admin.site.index_title = 'Panel de Control'
        admin.site.site_url = None