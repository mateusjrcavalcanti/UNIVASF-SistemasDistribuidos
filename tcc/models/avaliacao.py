from django.db import models
from django.conf import settings


def get_file_path_avaliacao(instance, filename):
    return os.path.join('tcc', f'{instance.tcc.id}', filename)


class Avaliacao(models.Model):
    avaliacao = models.FileField(
        upload_to=get_file_path_avaliacao, null=True, blank=True)

    avaliador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'groups__name': "Docentes"},
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.avaliador.get_full_name()} avaliou: {self.tcc.titulo} - {self.tcc.discente.get_full_name()}'

    class Meta:
        '''Meta definition for Post.'''
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
