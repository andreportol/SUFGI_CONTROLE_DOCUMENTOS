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
    assunto = models.CharField(_('Assunto'), max_length=120)
    data_entrada = models.DateField(_('Data de Entrada'), blank=False)
    data_saida = models.DateField(_('Data de Saída'),blank=True, null=True)
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
