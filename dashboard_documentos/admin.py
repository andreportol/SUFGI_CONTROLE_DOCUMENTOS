from django.contrib import admin
from .models import CadastroProcesso

@admin.register(CadastroProcesso)
class CadastroProcessoAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista de objetos
    list_display = ('numero_processo', 'requerente','assunto', 'data_entrada', 'data_saida','observacao','anexo','get_usuario')
    
    # Campos a serem filtrados na barra lateral
    #list_filter = ('data_entrada', 'data_saida')
    
    # Campos para busca na interface administrativa
    search_fields = ('numero_processo', 'requerente')
    
    # Campos que podem ser editados diretamente na lista de objetos
    list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_entrada',)
    
    # Serve para mostrar o nome do usuário que cadastrou o processo
    def save_model(self, request, obj, form, change):
        # Atribuir o request ao objeto para que ele possa ser usado no método save do modelo
        obj._request = request
        super().save_model(request, obj, form, change)
    
    # Método personalizado para exibir o nome do usuário
    def get_usuario(self, obj):
        if obj.usuario:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}" if obj.usuario.first_name and obj.usuario.last_name else obj.usuario.username
        return 'Usuário não definido'
    get_usuario.short_description = 'Cadastrado por:'

# Personalizando a interface administrativa
admin.site.site_header = 'SEMADUR - SUFGI'
admin.site.site_title = 'SUFGI'
admin.site.index_title = 'ADMINISTRAÇÃO'
