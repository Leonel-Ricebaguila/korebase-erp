#!/usr/bin/env python
"""
Script para establecer la contraseña del usuario admin
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'korebase.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Obtener usuario admin
try:
    user = User.objects.get(username='admin')
    
    # Establecer contraseña
    user.set_password('admin123')
    
    # Si necesita employee_id, establecerlo
    if not user.employee_id:
        user.employee_id = 'EMP-001'
    
    user.save()
    
    print("✅ Contraseña establecida exitosamente!")
    print("")
    print("📝 Credenciales:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("")
    print("🌐 Accede en: http://localhost:8001")
    
except User.DoesNotExist:
    print("❌ Usuario admin no encontrado")
except Exception as e:
    print(f"❌ Error: {e}")
