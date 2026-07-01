from django.db import models
from django.contrib.auth.models import User
from habitusapp.models.Professor import Professor
from habitusapp.models.Exercicio import Exercicio

class Treino(models.Model):
    NIVEIS = [
        ('I', 'Iniciante'),
        ('M', 'Intermediário'),
        ('A', 'Avançado'),
    ]
    
    nome = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    nivel = models.CharField(max_length=1, choices=NIVEIS, default='I')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True, null=True)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, blank=True, null=True)
    arquivado = models.BooleanField(default=False)

    @property
    def quant_exercicios(self):
        return self.exercicio.count()

    def __str__(self):
        return self.nome
