"""
URL configuration for korebase project.
Modular Monolith ERP System
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('core:dashboard'), name='home'),
    path('core/', include('core.urls')),
    path('logistica/', include('logistica.urls')),
    path('produccion/', include('produccion.urls')),
    path('financiero/', include('financiero.urls')),
]
