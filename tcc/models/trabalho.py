import os
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from tcc.models import Semestre


def get_file_path_trabalho(instance, filename):
    return os.path.join('tcc', f'{instance.id}', filename)


def get_file_path_avaliacao(instance, filename):
    return os.path.join('tcc', f'{instance.tcc.id}', filename)


class Trabalho(models.Model):
    TIPO_CHOICES = (
        ("I", "TCC I"),
        ("II", "TCC II")
    )

    titulo = models.CharField(max_length=250, null=True, blank=True)

    tipo = models.CharField(
        max_length=2, choices=TIPO_CHOICES, blank=False, null=False)

    anteprojeto = models.FileField(
        upload_to=get_file_path_trabalho, null=True, blank=True)

    discente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Discentes"},
        on_delete=models.CASCADE
    )

    orientador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Docentes"},
        related_name="orientacoes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    semestre = models.ForeignKey(
        Semestre,
        on_delete=models.CASCADE
    )

    homologacao_orientador = models.BooleanField(
        _('Homologação do anteprojeto (Orientador):'))
    homologacao_coordenador = models.BooleanField(
        _('Homologação do anteprojeto (Coordenador):'))

    def __str__(self):
        if self.titulo is not None:
            return f'TCC {self.tipo}: {self.titulo} - {self.discente.get_full_name()}'
        return f'TCC {self.tipo}: {self.discente.get_full_name()}'
