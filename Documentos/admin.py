from django.contrib import admin
from .models import Processo, Oficio, Setor, Servidor, CadastroEmail, OrdemServico

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('sigla_setor',)

    # Configura o campo ForeignKey para usar autocomplete
    search_fields = ['sigla_setor']
    
    # Define a ordem padrão dos objetos
    ordering = ('sigla_setor',)

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display= ('nome','setor_servidor','data_entrada','data_saida','ativo')

    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['setor_servidor']
    
    # Define a ordem padrão
    ordering = ('nome','ativo')

    search_fields = ('nome',)

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    # Define a ordem e a seleção dos campos exibidos na página de edição/detalhe de um modelo no Django Admin.
    fields = (
        'numero_processo', 
        'requerente', 
        'assunto',
        'data_abertura', 
        'setor', 
        'status', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    # Define quais colunas são exibidas na lista de objetos de um modelo (a visão em tabela no Django Admin). 
    list_display = ('numero_processo', 'requerente','assunto', 'data_abertura', 'setor','status','data_conclusao','observacao','anexo','get_usuario')
    
    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['setor']
    
    # Campos a serem filtrados na barra lateral
    #list_filter = ('data_entrada', 'data_saida')
    
    # Campos para busca na interface administrativa
    search_fields = ('numero_processo', 'requerente','assunto')
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_abertura',)
    
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
    # Define a ordem e a seleção dos campos exibidos na página de edição/detalhe de um modelo no Django Admin.
    fields = (
        'numero_oficio', 
        'assunto',
        'data_abertura',
        'prazo', 
        'setor', 
        'status', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    # Define quais colunas são exibidas na lista de objetos de um modelo (a visão em tabela no Django Admin).     
    list_display=('numero_oficio','assunto','data_abertura','prazo','data_vencimento','setor','status',
                  'data_conclusao','observacao', 'anexo')

    # Campos para busca na interface administrativa
    search_fields = ('numero_oficio', 'assunto','data_vencimento')
    
    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['setor']
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('data_vencimento',)

    def save_model(self, request, obj, form, change):
        obj._request = request
        super().save_model(request, obj, form, change)

@admin.register(CadastroEmail)
class EmailAdmin(admin.ModelAdmin):
    # Define a ordem e a seleção dos campos exibidos na página de edição/detalhe de um modelo no Django Admin.
    fields = (
        'remetente',
        'email',
        'assunto',
        'data_abertura', 
        'setor', 
        'status', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    list_display = ('remetente','email','assunto','setor','data_abertura',
                    'status','data_conclusao','observacao', 'anexo')

    # Campos para busca na interface administrativa
    search_fields = ('remetente','email','assunto')
    
    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['setor']

    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_abertura',)

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    # Define a ordem e a seleção dos campos exibidos na página de edição/detalhe de um modelo no Django Admin.
    fields = (
        'numero_os',
        'requerente',
        'assunto',
        'data_abertura', 
        'setor', 
        'status', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    
    list_display = ('numero_os','requerente','assunto','setor','data_abertura','status','data_conclusao','observacao')

    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['requerente', 'setor']

    # Campos para busca na interface administrativa
    search_fields = ('numero_os','assunto')
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_abertura',)

# Personalizando a interface administrativa
admin.site.site_header = 'SEMADUR - SUFGI'
admin.site.site_title = 'SUFGI'
admin.site.index_title = 'ADMINISTRAÇÃO'
