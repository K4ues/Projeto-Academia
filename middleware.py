"""
Middleware customizado para o projeto
"""
from django.utils.deprecation import MiddlewareMixin

class DisableCSRFCheckMiddleware(MiddlewareMixin):
    """
    Middleware para desabilitar verificação CSRF apenas em desenvolvimento.
    ATENÇÃO: Nunca use em produção!
    """
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
