from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    data = models.DateTimeField(default=now)
    conteudo = models.TextField()

    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"Notificação para {self.usuario.username} em {self.data.strftime('%d/%m/%Y %H:%M')}"
