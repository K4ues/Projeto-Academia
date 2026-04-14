from .settings import*
import os
DEBUG = True
#Crie secret key para seu ambiente de desenvolvimento
SECRET_KEY='ixb62ha#ts=ab4t2u%p1_62-!5w2j==j6d^3-j$!z(@*m+-h'
ALLOWED_HOSTS = ['*']  # Aceitar todos os hosts em desenvolvimento

# Configurações de segurança para desenvolvimento
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# Adicionar middleware para desabilitar CSRF em desenvolvimento
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'devadmin.middleware.DisableCSRFCheckMiddleware',  # Desabilita CSRF em dev
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

DATABASES={
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}

DATABASES={
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}