from django.db import models

class Exercicio(models.Model):
    class GrupoMuscularChoices(models.TextChoices):
        PEITO = 'Peito', 'Peito'
        OMBRO = 'Ombro', 'Ombro'
        BICEPS = 'Biceps', 'Biceps'
        DORSAL = 'Dorsal', 'Dorsal'
        TRICEPS = 'Triceps', 'Triceps'
        QUADRICEPS = 'Quadriceps', 'Quadriceps'
        GLUTEOS = 'Glúteos', 'Glúteos'
        ISQUIOTIBIAIS = 'Isquiotibiais', 'Isquiotibiais'
        PANTURRILHA = 'Panturrilha', 'Panturrilha'
        ABDOMINAIS = 'Abdominais', 'Abdominais'

    class DificuldadeChoices(models.TextChoices):
        INICIANTE = 'Iniciante', 'Iniciante'
        INTERMEDIARIO = 'Intermediário', 'Intermediário'
        AVANCADO = 'Avançado', 'Avançado'

    video = models.FileField(upload_to='videos-exercicios/', blank=True, null=True)
    imagem = models.ImageField(upload_to='imagens-exercicios/', null=True, blank=True)
    nome = models.CharField(max_length=100)
    grupo_muscular = models.CharField(
        max_length=20,
        choices=GrupoMuscularChoices.choices,
        default=GrupoMuscularChoices.PEITO
    )
    dificuldade = models.CharField(
        max_length=20,
        choices=DificuldadeChoices.choices,
        default=DificuldadeChoices.INICIANTE
    )
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
