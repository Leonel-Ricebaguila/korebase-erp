"""
Core Module - User Authentication and Base Models
KoreBase ERP System
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class Company(models.Model):
    """
    Representa a una entidad empresarial independiente (Tenant).
    El corazón de la arquitectura SaaS Multi-Tenant.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Razón Social / Nombre")
    rfc = models.CharField(max_length=13, blank=True, verbose_name="RFC")
    currency = models.CharField(
        max_length=3,
        default='MXN',
        choices=[('MXN', 'Peso Mexicano'), ('USD', 'Dólar Estadounidense')],
        verbose_name="Moneda Base"
    )
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    # Subscription & Billing
    SUBSCRIPTION_CHOICES = [
        ('starter', 'Starter'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    subscription_tier = models.CharField(
        max_length=20, 
        choices=SUBSCRIPTION_CHOICES, 
        default='starter'
    )
    is_trial = models.BooleanField(default=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.name} [{self.subscription_tier.upper()}]"


from core.managers import TenantManager

class TenantAwareModel(models.Model):
    """
    Clase base abstracta. TODO modelo operativo (Productos, Facturas, etc.)
    debe heredar de esta clase para aislarse por Empresa (SaaS).
    
    NOTA: company es null=True solo para compatibilidad con migración.
    Las vistas siempre deben asignar company = request.user.company al crear.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_related"
    )
    # Auditable fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Manager que filtra todo por el Request
    objects = TenantManager()

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Adds employee-specific fields for the ERP system
    """
    # Tenant Relationship
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="users",
        help_text="Empresa a la que pertenece este usuario (Tenant)"
    )

    # Override email to enforce uniqueness — critical for OAuth + OTP flows
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ID de Empleado",
        help_text="Identificador único del empleado"
    )
    department = models.CharField(
        max_length=100,
        verbose_name="Departamento",
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        blank=True
    )
    position = models.CharField(
        max_length=100,
        verbose_name="Puesto",
        blank=True
    )
    email_verified = models.BooleanField(
        default=False,
        verbose_name="Correo Verificado",
        help_text="Indica si el correo electrónico ha sido verificado"
    )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['employee_id']
    
    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name()}"


class Permission(models.Model):
    """
    Custom RBAC Permission System
    For granular access control across modules
    """
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    module = models.CharField(
        max_length=50,
        choices=[
            ('core', 'Core'),
            ('logistica', 'Logística'),
            ('produccion', 'Producción'),
            ('financiero', 'Financiero'),
        ]
    )
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        ordering = ['module', 'codename']
    
    def __str__(self):
        return f"{self.module}.{self.codename}"


class Role(models.Model):
    """
    Role model for RBAC
    Groups permissions together
    """
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')
    users = models.ManyToManyField(CustomUser, related_name='custom_roles')
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
    
    def __str__(self):
        return self.name


class OTPToken(models.Model):
    """
    One-Time Password token for email verification
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otp_tokens')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        from django.utils import timezone
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"OTP for {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Éxito'),
            ('error', 'Error'),
            ('info', 'Info'),
            ('warning', 'Advertencia')
        ],
        default='info'
    )
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type.upper()}] {self.user.username}: {self.message}"
