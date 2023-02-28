from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone


class Horario(models.Model):
    data = models.DateTimeField(_('Data:'))

    def __str__(self):
        return timezone.localtime(self.data).strftime('%d/%m/%Y %H:%M:%S')
