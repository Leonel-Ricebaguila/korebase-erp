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

try:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    
    # SIEMPRE establecer la contraseña, sea nuevo o existente
    user.set_password(password)
    user.email = email
    user.is_superuser = True
    user.is_staff = True
    user.save()

    if created:
        print(f'✅ Superusuario creado exitosamente: {username}')
    else:
        print(f'🔄 Superusuario existente actualizado: {username} (Contraseña reseteada)')

except Exception as e:
    print(f'❌ Error gestionando superusuario: {str(e)}')
