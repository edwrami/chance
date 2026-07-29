from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'DinnerPro'
    
    def ready(self):
        """
        Personalizar el admin cuando la app esté lista
        """
        from django.contrib import admin
        admin.site.site_header = 'DinnerPro Administración'
        admin.site.site_title = 'DinnerPro'
        admin.site.index_title = 'Panel de Control'
        admin.site.site_url = None