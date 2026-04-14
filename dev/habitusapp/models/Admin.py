from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Admin(models.Model):
    class Tipo_Trabalho(models.TextChoices):
        ADMIN = 'Administrador(a)', 'Administrador(a)'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    foto_perfil = models.ImageField(null=True, blank=True, upload_to='foto-perfil-admin/')
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    data_nasc = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo_trabalho = models.CharField(
        max_length=20,
        choices=Tipo_Trabalho.choices,
        default=Tipo_Trabalho.ADMIN
    )


    @property
    def idade(self):
        today = date.today()
        idade = today.year - self.data_nasc.year - ((today.month, today.day) < (self.data_nasc.month, self.data_nasc.day))
        return idade

    def __str__(self):
        return f"{self.nome} ({self.matricula}) ({self.idade}) ({self.data_criacao})"
