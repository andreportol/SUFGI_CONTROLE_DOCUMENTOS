from django.contrib import admin
from .models import Processo, Oficio, Setor, Servidor, CadastroEmail, OrdemServico, Tramitacao, Documento

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

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    search_fields = ['numero_documento','']  # Campo a ser usado para a busca no autocomplete

    def has_module_permission(self, request):
        # Isso oculta o modelo do menu principal do admin
        return False

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
        'responsavel', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    # Define quais colunas são exibidas na lista de objetos de um modelo (a visão em tabela no Django Admin). 
    list_display = ('numero_processo', 'requerente','assunto', 'data_abertura', 'setor','status','responsavel','data_conclusao','observacao','anexo','get_usuario')
    
    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['setor', 'responsavel']
    
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
        'responsavel', 
        'status', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    # Define quais colunas são exibidas na lista de objetos de um modelo (a visão em tabela no Django Admin).     
    list_display=('numero_oficio','assunto','data_abertura','prazo','data_vencimento','setor','status',
                  'responsavel','data_conclusao','observacao', 'anexo')

    # Campos para busca na interface administrativa
    search_fields = ('numero_oficio', 'assunto','data_vencimento')
    
    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['setor','responsavel']
    
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
        'responsavel', 
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
    autocomplete_fields = ['setor','responsavel']

    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_abertura',)

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    # Define a ordem e a seleção dos campos exibidos na página de edição/detalhe de um modelo no Django Admin.
    fields = (
        'numero_os',
        'responsavel',
        'assunto',
        'data_abertura', 
        'setor',
        'status', 
        'data_conclusao',
        'observacao', 
        'anexo',
    )
    
    list_display = ('numero_os','responsavel','assunto','setor','data_abertura','status','data_conclusao','observacao')

    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['responsavel', 'setor']

    # Campos para busca na interface administrativa
    search_fields = ('numero_os','assunto','responsavel__nome')
    
    # Campos que podem ser editados diretamente na lista de objetos
    #list_editable = ('data_saida',)
    
    # Define a ordem padrão dos objetos
    ordering = ('-data_abertura',)

@admin.register(Tramitacao)
class TramitacaoAdmin(admin.ModelAdmin):
    fields = ('num_documento', 'para','status')
    list_display = ('num_documento','get_de_nome_completo', 'get_para_nome_completo','criado','modificado','status')#,'criado','modificado')

    # Configura o campo ForeignKey para usar autocomplete
    autocomplete_fields = ['num_documento']

     
   # Campos para busca na interface administrativa
    search_fields = (
        'num_documento__processo__numero_processo', 
        'num_documento__oficio__numero_oficio', 
        'num_documento__ordemservico__numero_os', 
        'num_documento__cadastroemail__assunto'
    )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.de = request.user
        super().save_model(request, obj, form, change)
    
    def get_de_nome_completo(self, obj):
        return f"{obj.de.first_name} {obj.de.last_name}"
    get_de_nome_completo.short_description = 'De (Nome Completo)'

    
    def get_para_nome_completo(self, obj):
        return f"{obj.para.first_name} {obj.para.last_name}"
    get_para_nome_completo.short_description = 'Para (Nome Completo)'
   
# Personalizando a interface administrativa
admin.site.site_header = 'SEMADUR - SUFGI'
admin.site.site_title = 'SUFGI'
admin.site.index_title = 'ADMINISTRAÇÃO'
