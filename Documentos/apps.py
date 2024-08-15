from django.apps import AppConfig


class DashboardDocumentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Documentos'
    # Configura o painel admin do django para aparecer esse nome no lugar do nome da aplicação
    verbose_name = 'Administração'