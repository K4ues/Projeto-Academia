from django.contrib.auth.models import User
from django.db import models
from habitusapp.models import Treino, Exercicio

class TreinoExercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios_treino')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.PositiveIntegerField(default=0)
    repeticoes = models.PositiveIntegerField(default=0)
    carga = models.CharField(max_length=20, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.exercicio.nome} em {self.treino.nome}"
