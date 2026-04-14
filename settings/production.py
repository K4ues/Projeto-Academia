from .settings import *
import os
DEBUG = False
#Crie a secret key para seu ambiente de produção
SECRET_KEY = 'ixb6fha#ts=&b4t2u%p1_62-!8dw2j==j)d^3-j$!z(@*m+-h'
ALLOWED_HOSTS = ['localhost','127.0.0.1','habitus-2025.onrender.com','habitus-cnat.vercel.app',]

# Configurações de segurança para produção
CSRF_COOKIE_SECURE = True  # Apenas HTTPS
SESSION_COOKIE_SECURE = True  # Apenas HTTPS
SECURE_SSL_REDIRECT = True  # Redireciona HTTP para HTTPS

DATABASES = {
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}
