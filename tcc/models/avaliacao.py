import os
from django.db import models
from django.conf import settings
from tcc.models import Banca


def get_file_path_avaliacao(instance, filename):
    return os.path.join('tcc', f'{instance.banca.trabalho.id}', filename)


class Avaliacao(models.Model):
    avaliacao = models.FileField(
        upload_to=get_file_path_avaliacao, null=True)

    avaliador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Docentes"},
        on_delete=models.CASCADE
    )

    banca = models.ForeignKey(
        Banca,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f'{self.avaliador.get_full_name()} avaliou: {self.banca.trabalho.titulo} - {self.banca.trabalho.discente.get_full_name()}'

    class Meta:
        '''Meta definition for Post.'''
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
