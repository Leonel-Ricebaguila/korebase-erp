from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CompanyMembership, CompanyInvitation, Company


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser"""
    list_display = ['employee_id', 'username', 'first_name', 'last_name', 'company', 'department', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'department']
    search_fields = ['employee_id', 'username', 'first_name', 'last_name', 'email']

    fieldsets = UserAdmin.fieldsets + (
        ('Información de Empleado', {'fields': ('employee_id', 'department', 'phone', 'position', 'company', 'email_verified')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Empleado', {'fields': ('employee_id', 'department', 'phone', 'position')}),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'rfc', 'subscription_tier', 'is_trial', 'created_at']
    list_filter = ['subscription_tier', 'is_trial']
    search_fields = ['name', 'rfc']


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'joined_at']
    list_filter = ['role', 'company']
    search_fields = ['user__username', 'user__email', 'company__name']


@admin.register(CompanyInvitation)
class CompanyInvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'company', 'role', 'status', 'expires_at', 'invited_by']
    list_filter = ['status', 'role']
    search_fields = ['email', 'company__name']
    readonly_fields = ['token', 'created_at']
