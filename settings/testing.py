from .settings import *
import os
DEBUG=True
#Crie a secret key para seu ambiente de teste
SECRET_KEY = 'ixb6fh&#ts=&bt$au%pgp_62-!8dw2j==j)d^3-j$!z(@*m+-h'
ALLOWED_HOSTS = ['localhost','127.0.0.1','habitus-2025.onrender.com','habitus-cnat.vercel.app',]
DATABASES = {
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}