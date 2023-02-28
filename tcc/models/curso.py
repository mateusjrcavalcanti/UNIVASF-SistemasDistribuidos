from django.db import models


class Curso(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.nome)
