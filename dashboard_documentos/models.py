from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

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

class CadastroProcesso(Base):
    numero_processo = models.CharField(_('Número do Processo'), max_length=20, blank=False, unique=True)
    requerente = models.CharField(_('Requerente'), max_length=120, blank=False)
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
    data_entrada = models.DateField(_('Data de Entrada'), blank=False)
    data_saida = models.DateField(_('Data de Saída'),blank=True, null=True)
    TIPO_CHOICES_STATUS = (
        ('Aberto', 'Aberto'),
        ('Arquivado', 'Arquivado'),
        ('Atendido', 'Atendido'),
    )
    status = models.CharField(verbose_name='Status',
                              max_length=9, choices=TIPO_CHOICES_STATUS)
    observacao = models.TextField(verbose_name='Observações', max_length=400, blank=True)
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('Processo')
        verbose_name_plural = _('Processos')

    def __str__(self):
        return self.numero_processo

    def clean(self):
        # Validação personalizada para garantir que a data de entrada seja anterior à data de saída.
        if self.data_saida and self.data_entrada and self.data_entrada > self.data_saida:
            raise ValidationError(_('A data de entrada não pode ser posterior à data de saída.'))

    def save(self, *args, **kwargs):
        self.clean()  # Executa a validação ao salvar
        super().save(*args, **kwargs)
