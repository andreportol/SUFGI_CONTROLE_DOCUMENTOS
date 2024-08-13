from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import timedelta

User = get_user_model()

class Base(models.Model):
    criado = models.DateTimeField(_('Criação'), auto_now_add=True)
    modificado = models.DateTimeField(_('Atualização'), auto_now=True)
    usuario = models.ForeignKey(User, verbose_name=_('Usuário'), on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Atribuir o usuário atual ao campo 'usuario' antes de salvar
        if not self.id and hasattr(self, '_request') and self._request.user.is_authenticated:
            self.usuario = self._request.user
        super().save(*args, **kwargs)

class Setor(Base):
    sigla_setor = models.CharField(verbose_name='Setor', max_length=5, blank=False, help_text='Digite a sigla do setor.', unique=True)
    
    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
    
    def __str__(self):
        return self.sigla_setor

class Servidor(Base):        
    nome = models.CharField(verbose_name='Nome', max_length=120, blank=False, unique=True)
    setor_servidor = models.ForeignKey(Setor,verbose_name="Setor", on_delete=models.PROTECT)
    data_entrada = models.DateField(verbose_name='Data de entrada', blank=False)
    data_saida = models.DateField(verbose_name='Data de saída', blank=True, null=True)
    ativo = models.BooleanField(verbose_name='Ativo',default=True)
    
    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'
    
    def __str__(self):
        return self.nome

class Processo(Base):
    numero_processo = models.CharField(verbose_name= 'Número do Processo', max_length=20, blank=False, unique=True)
    requerente = models.CharField(verbose_name='Requerente', max_length=120, blank=False)
    TIPO_CHOICES_ASSUNTO = (
        ('ABERTURA DE INSCRICAO IMOBILIARIA AREA RURAL', 'Abertura de inscrição imobiliária área rural'),
        ('ABERTURA DE MATRICULA', 'Abertura de matrícula'),
        ('ABERTURA INSCRICAO IMOBILIARIA', 'Abertura inscrição imobiliária'),
        ('AQUISICAO DE MATERIAL PERMANENTE', 'Aquisição de material permanente'),
        ('APROVACAO DE PROJETOS ARQUITETONICO', 'Aprovação de projetos arquitetônico'),
        ('AUTO DE INFRACAO', 'Auto de infração'),
        ('AVERBACAO', 'Averbação'),
        ('AVERBACAO EX. OFICIO', 'Averbação ex. ofício'),
        ('BENEFICIO DO PRODES', 'Benefício do Prodes'),
        ('CANCELAMENTO DE DEBITO', 'Cancelamento de débito'),
        ('CERTIDAO', 'Certidão'),
        ('CERTIDAO DE DEMOLICAO', 'Certidão de demolição'),
        ('CERTIDAO DE EDIFICACAO', 'Certidão de edificação'),
        ('CERTIDAO DE VALOR VENAL', 'Certidão de valor venal'),
        ('CERTIDAO EDIFICACAO – LEI 13.865/2019', 'Certidão edificação – Lei 13.865/2019'),
        ('CONTRATACAO DE SERVICO', 'Contratação de serviço'),
        ('DEMANDA DE SOFTWARES DO SETOR', 'Demanda de softwares do setor'),
        ('DESAFETACAO', 'Desafetação'),
        ('DESAPROPRIACAO', 'Desapropriação'),
        ('DESM/REMEM/DESDOBRO E AVERBACAO', 'Desm/remem/desdobro e averbação'),
        ('DOACAO DE AREA', 'Doação de área'),
        ('DOACAO EM PAGAMENTO', 'Doação em pagamento'),
        ('ISENCAO DE IPTU', 'Isenção de IPTU'),
        ('ISENCAO DE ITBI RURAL', 'Isenção de ITBI rural'),
        ('ISENCAO DE ITBI URBANO', 'Isenção de ITBI urbano'),
        ('INDENIZACAO', 'Indenização'),
        ('LEVANTAMENTO TOPOGRAFICO', 'Levantamento topográfico'),
        ('LOTEAMENTO', 'Loteamento'),
        ('NOTIFICACAO DE AUTO DE INFRACAO', 'Notificação de auto de infração'),
        ('OUTRO ASSUNTO','Outro assunto'),
        ('PARECERES', 'Pareceres'),
        ('PARECER IMOBILIARIO', 'Parecer imobiliário'),
        ('PARCELAMENTO', 'Parcelamento'),
        ('PERMUTA', 'Permuta'),
        ('PERMISSAO DE USO DE AREA PUBLICA', 'Permissão de uso de área pública'),
        ('PRESTACAO DE SERVICOS DIVERSOS', 'Prestação de serviços diversos'),
        ('PROCESSO DE APOSENTADORIA E PENSIONISTA', 'Processo de aposentadoria e pensionista'),
        ('PROCESSO DE DEBITO', 'Processo de débito'),
        ('REGULARIZACAO', 'Regularização'),
        ('REGULARIZACAO FUNDIARIA', 'Regularização fundiária'),
        ('REMEMBRAMENTO/DESDOBRO', 'Remembramento/desdobro'),
        ('REVISAO DE DADOS CADASTRAIS', 'Revisão de dados cadastrais'),
        ('REAVALIACAO DE ITBI RURAL', 'Reavaliação de ITBI rural'),
        ('REAVALIACAO DE ITBI URBANO', 'Reavaliação de ITBI urbano'),
        ('SUBSTITUICAO DE RESPONS TRIBUTARIO', 'Substituição de respons tributário'),
        ('SUBSTITUICAO DE PROJETO', 'Substituição de projeto'),
        ('VERIFICACAO', 'Verificação'),
        ('VERIFICACAO DE IPTU', 'Verificação de IPTU'),
        ('VERIFICACAO DE I.P.T.U.', 'Verificação de I.P.T.U.'),
        ('REQUERIMENTO', 'Requerimento'),
    )
    assunto = models.CharField(verbose_name='Tipo de Assunto', max_length=255, choices=TIPO_CHOICES_ASSUNTO, blank=False)
    data_abertura_processo = models.DateField(_('Data de abertura'), blank=False, help_text='Informe a data de abertura do Processo.')
    setor_processo = models.ForeignKey(Setor, verbose_name='Setor', on_delete=models.PROTECT)
    TIPO_CHOICES_STATUS = (
        ('Aberto', 'Aberto'),
        ('Arquivado', 'Arquivado'),
        ('Concluido', 'Concluído'),
    )
    status = models.CharField(verbose_name='Status',
                              max_length=9, choices=TIPO_CHOICES_STATUS, default='Aberto')
    data_conclusao_processo = models.DateField(_('Data de conclusão'), blank=True,null=True, help_text='Informe a data de conclusão do Processo.')
    observacao = models.TextField(verbose_name='Observações', max_length=400, blank=True)
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('Processo')
        verbose_name_plural = _('Processos')

    def __str__(self):
        return self.numero_processo

    def clean(self):
        # Validação personalizada para garantir que a data de entrada seja anterior à data de saída.
        if self.data_conclusao_processo and self.data_abertura_processo and self.data_abertura_processo > self.data_conclusao_processo:
            raise ValidationError(_('A data de cadastro não pode ser posterior à data de conclusão.'))

    def save(self, *args, **kwargs):
        self.clean()  # Executa a validação ao salvar
        super().save(*args, **kwargs)

class Oficio(Base):
    numero_oficio = models.CharField('Número do Ofício', max_length=20, blank=False, unique=True)
    assunto = models.CharField(verbose_name='Assunto', max_length=100, blank=False)
    setor_oficio = models.ForeignKey(Setor, verbose_name='Setor', on_delete= models.PROTECT)
    data_oficio = models.DateField(verbose_name='Data do ofício', blank=False, help_text='Digite a data do ofício.')
    prazo = models.PositiveSmallIntegerField(verbose_name='Prazo', help_text='Quantidade de dias.', blank=False)
    data_vencimento = models.DateField(verbose_name='Data de vencimento', blank=True, editable=False)
    TIPO_CHOICES_STATUS = (
        ('Aberto', 'Aberto'),
        ('Arquivado', 'Arquivado'),
        ('Atendido', 'Atendido'),
    )
    status = models.CharField(verbose_name='Status',
                              max_length=9, choices=TIPO_CHOICES_STATUS, default= 'Aberto')
    data_conclusao_oficio = models.DateField(verbose_name='Data de conclusão',blank=True, null=True)
    observacao = models.TextField(verbose_name='Observações', max_length=400, blank=True)
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)
    
    class Meta:
        verbose_name = ('Ofício')
        verbose_name_plural = ('Ofícios')

    def __str__(self):
        return self.numero_oficio

    def save(self, *args, **kwargs):
        # Calcula a data de vencimento baseada na data do ofício e no prazo
        if self.data_oficio and self.prazo:
            self.data_vencimento = self.data_oficio + timedelta(days=self.prazo)
        super().save(*args, **kwargs)