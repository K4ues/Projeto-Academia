from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Noticia(models.Model):
    class CategoriaChoices(models.TextChoices):
        AVISO_IMPORTANTE = 'AVISO IMPORTANTE', 'Aviso Importante'
        EVENTO = 'EVENTO', 'Evento'

    imagem = models.ImageField(upload_to='noticias/', blank=True, null=True)
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaChoices.choices,
        default=CategoriaChoices.AVISO_IMPORTANTE
    )
    descricao = models.TextField(blank=True, null=True)
    data_publicacao = models.DateTimeField(default=datetime.now)

    autor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    autor_nome = models.CharField(max_length=100)
    autor_tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.descricao} - {self.autor_nome}"
