import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
from tcc.models import Curso

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


class Semestre(models.Model):
    '''Model definition for Semestre.'''
    coordenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Docentes"},
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE
    )
    ano = models.IntegerField(
        _('Ano'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    numero = models.IntegerField(_('Semestre'), validators=[MinValueValidator(0),
                                                            MaxValueValidator(3)])
    reuniaoInicial = models.DateTimeField(
        _('Reunião Inicial'), null=True, blank=True)
    confirmacaoMatricula = models.DateTimeField(
        _('Confirmação de Matrícula'), null=True, blank=True)
    homologacaoAnteprojeto = models.DateTimeField(
        _('Homologação dos Anteprojetos'), null=True, blank=True)
    resultadosAnteprojeto = models.DateTimeField(
        _('Divulgação do resultado dos anteprojetos'), null=True, blank=True)
    formularioAcompanhamento = models.DateTimeField(
        _('Formulário de Acompanhamento'), null=True, blank=True)
    definicaoBanca = models.DateTimeField(
        _('Definição das Bancas de Defesa'), null=True, blank=True)
    homologacaoBanca = models.DateTimeField(
        _('Homologação/divulgação das Bancas'), null=True, blank=True)
    inicioDefesas = models.DateTimeField(
        _('Início do período de defesas'), null=True, blank=True)
    fimDefesas = models.DateTimeField(
        _('Fim do período de defesas'), null=True, blank=True)
    envio = models.DateTimeField(
        _('Envio da versão final'), null=True, blank=True)
    publicacaoUm = models.DateTimeField(
        _('Publicação de notas de TCC I'), null=True, blank=True)
    publicacaoDois = models.DateTimeField(
        _('Publicação de notas de TCC II'), null=True, blank=True)

    class Meta:
        '''Meta definition for Post.'''
        verbose_name = 'Semestre'
        verbose_name_plural = 'Semestres'

    def __str__(self):
        return "%s.%s" % (self.ano, self.numero)
