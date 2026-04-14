#!/usr/bin/env python
"""
Script de teste para verificar configurações CSRF
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devadmin.settings.development')
sys.path.insert(0, '/workspaces/academia-cnat/dev')
django.setup()

from django.conf import settings
from django.test import Client
from django.middleware.csrf import get_token

print("=" * 60)
print("TESTE DE CONFIGURAÇÕES CSRF")
print("=" * 60)
print(f"\n✓ DEBUG: {settings.DEBUG}")
print(f"✓ CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"✓ SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"✓ CSRF_COOKIE_HTTPONLY: {settings.CSRF_COOKIE_HTTPONLY}")
print(f"✓ CSRF_COOKIE_SAMESITE: {settings.CSRF_COOKIE_SAMESITE}")
print(f"✓ CSRF_USE_SESSIONS: {settings.CSRF_USE_SESSIONS}")
print(f"✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✓ CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")

print("\n" + "=" * 60)
print("TESTE DE REQUISIÇÃO COM CSRF TOKEN")
print("=" * 60)

# Criar cliente de teste
client = Client()

# Fazer requisição GET na página de login
response = client.get('/')
print(f"\n✓ GET /login - Status: {response.status_code}")
print(f"✓ Cookies recebidos: {list(response.cookies.keys())}")

# Verificar se o CSRF token está no cookie
if 'csrftoken' in response.cookies:
    csrf_token = response.cookies['csrftoken'].value
    print(f"✓ CSRF Token obtido: {csrf_token[:20]}...")
    
    # Tentar fazer POST com o token
    response_post = client.post('/', {
        'email': 'teste@teste.com',
        'senha': 'senha123'
    })
    
    print(f"\n✓ POST /login - Status: {response_post.status_code}")
    
    if response_post.status_code == 403:
        print("✗ ERRO 403: CSRF token falhou!")
        print("  Verifique se o middleware CsrfViewMiddleware está ativo")
    else:
        print("✓ CSRF token aceito com sucesso!")
else:
    print("✗ ERRO: Cookie csrftoken não foi criado!")
    print("  Verifique o middleware SessionMiddleware e CsrfViewMiddleware")

print("\n" + "=" * 60)
