import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.conf import settings
from tcc.models import Horario, Trabalho, Resultado, Avaliacao


class Banca(models.Model):

    avaliadores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='avaliacoes',
        limit_choices_to={'groups__name': "Docentes"},
    )

    coorientadores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='coorientacoes',
        limit_choices_to={'groups__name': "Docentes"},
        blank=True
    )

    horario = models.OneToOneField(
        Horario,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    trabalho = models.OneToOneField(
        Trabalho,
        on_delete=models.SET_NULL,
        null=True
    )

    resultado = models.OneToOneField(
        Resultado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    avaliacoesresult = models.ManyToManyField(
        Avaliacao,
        related_name='avaliacoesresult',
        blank=True
    )

    homologacao_orientador = models.BooleanField(
        _('Homologação do Orientador:'))
    homologacao_coordenador = models.BooleanField(
        _('Homologação do Coordenador:'))

    def __str__(self):
        if self.horario is not None:
            return f'{self.trabalho.discente.get_full_name()} - {self.trabalho.titulo}  - {self.horario}'
        return f'{self.trabalho.discente.get_full_name()} - {self.trabalho.titulo}'
