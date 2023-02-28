from django.db import models
from django.utils.translation import gettext as _


class Resultado(models.Model):
    cidade = models.CharField(
        _('Localização:'), max_length=250, default='Juazeiro/BA')
    inicio = models.DateTimeField(_('Inicio:'))
    fim = models.TimeField(_('Fim:'))
    aprovado = models.BooleanField(_('Aprovado?'))
    media = models.FloatField(_('Média Final:'))

    def __str__(self):
        if self.aprovado:
            status = 'Aprovado'
        else:
            status = 'Reprovado'
        return f'{self.tcc.discente.get_full_name()} - {status}'
