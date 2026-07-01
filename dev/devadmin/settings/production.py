from .settings import *
import os
DEBUG = False
SECRET_KEY = 'ixb6fha#ts=&b4t2u%p1_62-!8dw2j==j)d^3-j$!z(@*m+-h'
ALLOWED_HOSTS = ['localhost','127.0.0.1','habitus-2025.onrender.com','habitus-cnat.vercel.app',]

CSRF_COOKIE_SECURE = True 
SESSION_COOKIE_SECURE = True  
SECURE_SSL_REDIRECT = True 

DATABASES = {
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}
