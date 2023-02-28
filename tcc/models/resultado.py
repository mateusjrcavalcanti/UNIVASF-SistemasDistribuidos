import os
from django.db import models
from django.utils.translation import gettext as _
from tcc.models import Banca


def get_file_path(instance, filename):
    return os.path.join('tcc', f'{instance.id}', filename)


class Resultado(models.Model):
    cidade = models.CharField(
        _('Localização:'), max_length=250, default='Juazeiro/BA')
    inicio = models.DateTimeField(_('Inicio:'))
    fim = models.TimeField(_('Fim:'))
    aprovado = models.BooleanField(_('Aprovado?'))
    media = models.FloatField(_('Média Final:'))

    banca = models.OneToOneField(
        Banca,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    documento = models.FileField(
        upload_to=get_file_path, null=True, blank=True)

    def __str__(self):
        if self.aprovado:
            status = 'Aprovado'
        else:
            status = 'Reprovado'
        return f'{self.banca.trabalho.discente.get_full_name()} - {status}'
