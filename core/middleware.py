import threading

_thread_locals = threading.local()

def get_current_company():
    """
    Retorna la empresa ('Company') asociada al hilo web actual.
    """
    return getattr(_thread_locals, 'company', None)

class ThreadLocalTenantMiddleware:
    """
    Middleware Multi-Tenant: Extrae silenciosamente la empresa
    del usuario autenticado y la guarda en la memoria del hilo de la request
    para que los TenantManagers la utilicen automáticamente sin que el
    desarrollador deba pasarla manualmente.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Obtenemos el Tenant del request (si está logueado)
        if request.user.is_authenticated and hasattr(request.user, 'company'):
            _thread_locals.company = request.user.company
        else:
            _thread_locals.company = None

        # 2. Dejamos que Django haga su magia (pasamos a la vista)
        response = self.get_response(request)

        # 3. Limpieza: por seguridad borramos el tenant al finalizar la request
        if hasattr(_thread_locals, 'company'):
            del _thread_locals.company

        return response
