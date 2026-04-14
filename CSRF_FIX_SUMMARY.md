# Correções Aplicadas para Resolver Erro CSRF Intermitente

## Data: 27/11/2025

## Problemas Identificados:

1. **Decoradores Conflitantes**: Uso de `@csrf_exempt` seguido de `@csrf_protect` anulava a proteção CSRF
2. **CSRF_TRUSTED_ORIGINS Incorreto**: Incluía `https://localhost:8000` (inválido para desenvolvimento)
3. **Falta de Configurações Explícitas**: Ausência de configurações de cookies CSRF
4. **ALLOWED_HOSTS Restritivo**: Em desenvolvimento com codespaces/containers, precisa aceitar hosts dinâmicos

## Arquivos Modificados:

### 1. `/dev/devadmin/settings/settings.py`
- Adicionado configurações de CSRF e Session cookies
- Corrigido CSRF_TRUSTED_ORIGINS (removido https://localhost:8000)

### 2. `/dev/devadmin/settings/development.py`
- Alterado ALLOWED_HOSTS para ['*'] (desenvolvimento)
- Adicionado CSRF_TRUSTED_ORIGINS específicas
- Explicitamente definido CSRF_COOKIE_SECURE = False
- Explicitamente definido SESSION_COOKIE_SECURE = False

### 3. `/dev/devadmin/settings/production.py`
- Adicionado configurações de segurança para produção
- CSRF_COOKIE_SECURE = True
- SESSION_COOKIE_SECURE = True
- SECURE_SSL_REDIRECT = True

### 4. Views corrigidas (removido @csrf_exempt conflitante):
- **viewsUsuario.py**: login, criar_conta, excluir_treino, novo_treino, editar_treino, apagar_todos_treinos, zerar_progresso, comecar_treino
- **viewsProfessor.py**: atualizar_foto_aluno, editar_aluno, excluir_treino_professor, editar_treino_professor
- **viewsAdmin.py**: novo_professor, atualizar_foto_professor, editar_professor, exercicios, novo_exercicio, excluir_exercicio, editar_exercicio

## Configurações Aplicadas:

```python
# Em settings.py (base)
CSRF_COOKIE_SECURE = False  # True apenas em produção
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False  # True apenas em produção
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# Em development.py
ALLOWED_HOSTS = ['*']  # Aceita qualquer host em dev
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost',
    'http://127.0.0.1',
]
```

## Teste Realizado:

✅ Script de teste confirmou que CSRF está funcionando corretamente
✅ GET /login retorna status 200 com cookie csrftoken
✅ POST /login aceita o token corretamente

## Próximos Passos:

1. Limpar cookies do navegador (Ctrl+Shift+Delete)
2. Acessar a aplicação em modo anônimo ou após limpar cookies
3. Testar login, logout e operações CRUD (especialmente exclusões)

## Notas Importantes:

- **Desenvolvimento**: Use `devadmin.settings.development` (já configurado no manage.py)
- **Produção**: Use `devadmin.settings.production` com variável de ambiente
- Em produção, reverter ALLOWED_HOSTS para lista específica de domínios
- Nunca usar `@csrf_exempt` a menos que seja uma API externa sem autenticação
