from django.apps import AppConfig


class MemoryMapsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'memory_maps'
    verbose_name = 'Personal Memory Maps'
    
    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        pass  # Import signals here when needed
