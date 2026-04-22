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


class CompanyMembership(models.Model):
    """
    Tabla pivote: relaciona un Usuario con una Empresa y define su Rol.
    Es la única fuente de verdad para el control de acceso (RBAC) del tenant.

    REGLAS:
      - owner:    Creador original. No puede ser removido. Acceso total + puede invitar.
      - admin:    Acceso operativo total. Puede invitar a otros.
      - operator: Puede crear/editar registros en todos los módulos. No puede eliminar ni invitar.
      - viewer:   Solo lectura en todos los módulos.

    INVARIANTE: Un usuario sólo puede tener UNA membresía por empresa (unique_together).
    Si un email ya tiene cuenta, no puede unirse a otra empresa (Opción A - Aislamiento Estricto).
    """
    ROLE_CHOICES = [
        ('owner',    'Propietario'),
        ('admin',    'Administrador'),
        ('operator', 'Operador'),
        ('viewer',   'Espectador'),
    ]

    user      = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='memberships')
    company   = models.ForeignKey(Company,    on_delete=models.CASCADE, related_name='memberships')
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Membresía de Empresa"
        verbose_name_plural = "Membresías"
        unique_together = [['user', 'company']]
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user.username} @ {self.company.name} [{self.role.upper()}]"

    @property
    def is_owner(self):
        return self.role == 'owner'

    @property
    def can_invite(self):
        """Solo owner y admin pueden generar invitaciones."""
        return self.role in ('owner', 'admin')

    @property
    def can_write(self):
        """owner, admin y operator pueden crear/editar. viewer es solo lectura."""
        return self.role in ('owner', 'admin', 'operator')


class CompanyInvitation(models.Model):
    """
    Token criptográfico de un solo uso para invitar a un colaborador a una empresa.

    Flujo completo:
      1. Dueño/Admin genera invitación → se crea este registro con token UUID único.
      2. Se envía un correo con el link /core/join/<token>/ al email del invitado.
      3. El invitado abre el link:
         a) Sin cuenta → redirige a /registro/, token se guarda en sesión.
            Al verificar OTP, se asigna a la empresa de la invitación (NO crea empresa propia).
         b) Con cuenta del mismo email → acepta directamente.
         c) Con cuenta de OTRO email → error 403 (Opción A: aislamiento estricto).
      4. Al aceptar: se crea CompanyMembership con el rol especificado.
         El token pasa a estado 'accepted' (no reutilizable).

    SEGURIDAD:
      - El token es un UUID4 (122 bits de entropía — no predecible).
      - La invitación expira automáticamente a las 48 horas.
      - Un token usado o expirado nunca puede activarse de nuevo.
    """
    STATUS_CHOICES = [
        ('pending',  'Pendiente'),
        ('accepted', 'Aceptada'),
        ('expired',  'Expirada'),
        ('revoked',  'Revocada'),
    ]

    company     = models.ForeignKey(Company,     on_delete=models.CASCADE,  related_name='invitations')
    invited_by  = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, related_name='sent_invitations')
    email       = models.EmailField(verbose_name="Correo del Invitado")
    role        = models.CharField(max_length=20, choices=CompanyMembership.ROLE_CHOICES, default='operator')
    token       = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    expires_at  = models.DateTimeField()
    accepted_by = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_invitations')
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Invitación"
        verbose_name_plural = "Invitaciones"
        ordering = ['-created_at']

    def __str__(self):
        return f"Invitación → {self.email} a {self.company.name} [{self.status.upper()}]"

    @property
    def is_valid(self):
        """Un token es válido solo si está pendiente Y no ha expirado."""
        return self.status == 'pending' and self.expires_at > timezone.now()


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
