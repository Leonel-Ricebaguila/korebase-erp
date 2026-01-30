"""
Core Module - User Authentication and Base Models
KoreBase ERP System
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Adds employee-specific fields for the ERP system
    """
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
