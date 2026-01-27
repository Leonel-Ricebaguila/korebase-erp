from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Permission, Role


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser"""
    list_display = ['employee_id', 'username', 'first_name', 'last_name', 'department', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'department']
    search_fields = ['employee_id', 'username', 'first_name', 'last_name', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Empleado', {'fields': ('employee_id', 'department', 'phone', 'position')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Empleado', {'fields': ('employee_id', 'department', 'phone', 'position')}),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['codename', 'name', 'module']
    list_filter = ['module']
    search_fields = ['name', 'codename']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['permissions', 'users']
