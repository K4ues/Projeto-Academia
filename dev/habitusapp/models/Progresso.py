from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  # se estiver usando PostgreSQL


class Progresso(models.Model):
    class NivelChoices(models.TextChoices):
        INICIANTE = 'Iniciante', 'Iniciante'
        INTERMEDIARIO = 'Intermediário', 'Intermediário'
        AVANCADO = 'Avançado', 'Avançado'
    class ObjetivoChoices(models.TextChoices):
        GANHODEMASSA = 'Ganho de Massa', 'Ganho de Massa'
        PERDADEPESO = 'Perda de peso', 'Perda de peso'
        SAUDE = 'Saúde', 'Saúde'
        OUTRO = 'Outro', 'Outro'
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    peso = models.FloatField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    nivel = models.CharField(
        max_length=20,
        choices=NivelChoices.choices,
        blank=True, null=True
    )
    objetivo = models.CharField(
        max_length=20,
        choices=ObjetivoChoices.choices,
        blank=True, null=True
    )
    data_entrada = models.DateField(default=date.today)
    progresso_valor = models.IntegerField(default=0)
    concluidos = models.IntegerField(default=0)
    dias_treinados = models.JSONField(default=list, blank=True)
    ultimo_treino_id = models.IntegerField(blank=True, null=True)  # Novo campo para ciclo de treinos

    #Medição das cincunfêrencias
    cintura = models.FloatField(blank=True, null=True)
    abdomen = models.FloatField(blank=True, null=True)
    torax = models.FloatField(blank=True, null=True)
    quadril = models.FloatField(blank=True, null=True)
    coxa_direita = models.FloatField(blank=True, null=True)
    coxa_esquerda = models.FloatField(blank=True, null=True)
    panturrilha_direita = models.FloatField(blank=True, null=True)
    panturrilha_esquerda = models.FloatField(blank=True, null=True)
    braco_direito = models.FloatField(blank=True, null=True)
    braco_esquerdo = models.FloatField(blank=True, null=True)

    #Medições das dobras cutâneas
    tricipital = models.FloatField(blank=True, null=True)
    subescapular = models.FloatField(blank=True, null=True)
    axilar_media = models.FloatField(blank=True, null=True)
    suprailiaca = models.FloatField(blank=True, null=True)
    abdominal = models.FloatField(blank=True, null=True)
    coxa = models.FloatField(blank=True, null=True)
    panturrilha= models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario} ({self.nivel})"
