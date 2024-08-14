from django.contrib import admin
from .models import Processo, Oficio, Setor, Servidor, CadastroEmail

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('sigla_setor',)
    
    # Define a ordem padrão dos objetos
    ordering = ('sigla_setor',)

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display= ('nome','setor_servidor','data_entrada','data_saida','ativo')

    # Define a ordem padrão
    ordering = ('nome','ativo')

    search_fields = ('nome',)

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista de objetos
    list_display = ('numero_processo', 'requerente','assunto', 'data_abertura_processo', 'setor_processo','status','data_conclusao_processo','observacao','anexo','get_usuario')
    
    # Campos a serem filtrados na barra lateral
    #list_filter = ('data_entrada', 'data_saida')
    
    # Campos para busca na interface administrativa
    search_fields = ('numero_processo', 'requerente','assunto')
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_abertura_processo',)
    
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

@admin.register(Oficio)
class OficioAdmin(admin.ModelAdmin):
    list_display=('numero_oficio','assunto','setor_oficio','data_oficio','prazo','data_vencimento','status',
                  'data_conclusao_oficio','observacao', 'anexo')

    # Campos para busca na interface administrativa
    search_fields = ('numero_oficio', 'assunto','data_vencimento')
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_oficio',)

    def save_model(self, request, obj, form, change):
        obj._request = request
        super().save_model(request, obj, form, change)

@admin.register(CadastroEmail)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('remetente','email','assunto','setor_email','data_email',
                    'status','data_conclusao','observacao')

    # Campos para busca na interface administrativa
    search_fields = ('remetente','email_rementente','assunto')
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_email',)


# Personalizando a interface administrativa
admin.site.site_header = 'SEMADUR - SUFGI'
admin.site.site_title = 'SUFGI'
admin.site.index_title = 'ADMINISTRAÇÃO'
