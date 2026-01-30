#!/usr/bin/env python
"""
Script para crear superusuario automáticamente en deployment
Usa variables de entorno para seguridad
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Obtener credenciales desde variables de entorno
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@korebase.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Verificar si el superusuario ya existe
if not User.objects.filter(username=username).exists():
    print(f'👤 Creando superusuario: {username}')
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print('✅ Superusuario creado exitosamente!')
else:
    print(f'ℹ️  Superusuario "{username}" ya existe, omitiendo creación.')
