from django.db import models
from core.middleware import get_current_company


class TenantQuerySet(models.QuerySet):
    """
    QuerySet personalizado para inyectar filtros automáticos de Tenant.
    """
    def as_manager(cls):
        manager = TenantManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager
    as_manager.queryset_only = True


class TenantManager(models.Manager):
    """
    SaaS Manager: Sobrescribe la función fundamental .get_queryset()
    para filtrar silenciosamente los registros de acuerdo a la 
    Empresa extraída del ThreadLocal (la que visitó la pestaña del ERP).
    """

    def get_queryset(self):
        # 1. Obtenemos el QuerySet normal de Django
        qs = super().get_queryset()

        # 2. Le preguntamos al Middleware ¿Quién está haciendo la petición?
        company = get_current_company()

        # 3. Si hay una empresa asignada al hilo, inyectarle el '.filter(company=Company)' forzoso
        if company:
            return qs.filter(company=company)
        
        # Ojo: Si la tarea corre por detrás (Celery/Cronjobs) o en modo consola, 
        # get_current_company() podría devolver None. Evaluaremos luego si
        # bloquear el acceso sin Tenant para total seguridad, o permitir el global.
        # Por ahora bloqueamos por seguridad (Zero-Trust Model) a menos que esté documentado
        return qs.filter(company=None) # Si no hay Company en el request, no enseña NADA
