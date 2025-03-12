from django.apps import AppConfig

class WorkspacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.workspaces'

    def ready(self):
        import apps.workspaces.infrastructure.models
