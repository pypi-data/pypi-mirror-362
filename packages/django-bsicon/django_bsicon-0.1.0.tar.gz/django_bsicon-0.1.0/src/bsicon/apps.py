from django.apps import AppConfig

class BsiconConfig(AppConfig):
    # Nombre canónico de la aplicación (debe coincidir con el nombre del paquete)
    name = 'bsicon'
    
    # Nombre legible para humanos (aparecerá en el admin de Django)
    verbose_name = 'Bootstrap Icons'
    
    # Configuración por defecto para el campo de iconos
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está completamente cargada.
        Aquí podemos realizar inicializaciones y registrar señales.
        """
        # Importamos los widgets para asegurar su registro
        from . import widgets  # noqa: F401
        
        # (Opcional) Podemos agregar lógica de inicialización aquí
        # Ej: Verificar si los archivos de iconos están presentes
        self.verify_static_files()
    
    def verify_static_files(self):
        """
        Verifica que los archivos estáticos críticos estén presentes.
        Útil durante el desarrollo para detectar problemas de configuración.
        """
        import os
        from django.conf import settings
        from django.core.checks import Warning, register
        
        # Lista de archivos críticos que deben existir
        critical_files = [
            'bsicon/css/bootstrap-icons.min.css',
            'bsicon/fonts/bootstrap-icons.woff2',
            'bsicon/js/bsicon.js'
        ]
        
        @register('bsicon')
        def check_static_files(app_configs, **kwargs):
            errors = []
            for file_path in critical_files:
                full_path = os.path.join(settings.STATIC_ROOT, file_path) if settings.STATIC_ROOT \
                           else os.path.join(settings.BASE_DIR, 'static', file_path)
                
                if not os.path.exists(full_path):
                    errors.append(
                        Warning(
                            f'Archivo estático faltante: {file_path}',
                            hint=('Ejecuta `python manage.py collectstatic` o verifica tu instalación'),
                            obj=self,
                            id='bsicon.W001',
                        )
                    )
            return errors
