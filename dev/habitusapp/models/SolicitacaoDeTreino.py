from django.db import models
from django.conf import settings
from django.utils import timezone
from habitusapp.models import Professor  # importa Professor do app certo

class SolicitacaoDeTreino(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aberta'),
        ('C', 'Concluída'),
        ('R', 'Recusada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitacoes')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='solicitacoes')
    descricao = models.TextField(max_length=2000, blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    def __str__(self):
        return f"{self.usuario} → {self.professor} ({self.get_status_display()})"
