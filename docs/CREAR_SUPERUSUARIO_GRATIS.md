# 🔐 GUÍA: Crear Superusuario sin Shell (Gratis)

## 🎯 **ALTERNATIVA 1: Creación Automática en Build** ⭐ (RECOMENDADA)

Esta solución crea el superusuario **automáticamente** durante el deployment, sin necesidad del Shell de pago.

---

## 📋 **PASOS A SEGUIR**

### **Paso 1: Agregar Variables de Entorno en Render** 🔑

1. Ve a **Render.com** → Tu servicio **korebase-erp**
2. Haz clic en **"Environment"** (en el menú lateral)
3. Haz clic en **"Add Environment Variable"**
4. Agrega las siguientes **3 variables**:

#### **Variable 1: Username**
```
Key:   DJANGO_SUPERUSER_USERNAME
Value: admin
```

#### **Variable 2: Email**
```
Key:   DJANGO_SUPERUSER_EMAIL
Value: admin@korebase.com
```

#### **Variable 3: Password** ⚠️ IMPORTANTE
```
Key:   DJANGO_SUPERUSER_PASSWORD
Value: [TU_CONTRASEÑA_SEGURA]
```

**⚠️ IMPORTANTE**: 
- **NO uses** `admin123` en producción
- Usa una contraseña **SEGURA** como: `KoreBase2026!Secure`
- Guarda esta contraseña en un lugar seguro

5. Haz clic en **"Save Changes"**

---

### **Paso 2: Hacer Commit y Push** 📤

Los archivos ya están listos:
- ✅ `create_superuser.py` (script de creación)
- ✅ `build.sh` (actualizado con el paso de creación)

Ahora solo necesitas hacer commit y push:

```bash
git add create_superuser.py build.sh
git commit -m "feat: agregar creación automática de superusuario en deployment"
git push origin main
```

---

### **Paso 3: Esperar el Re-Deployment** ⏳

Render detectará el nuevo commit y re-desplegará automáticamente.

**Durante el build verás**:
```
🚀 Installing dependencies...
📦 Collecting static files...
🗄️  Running database migrations...
👤 Creating superuser (if not exists)...
✅ Superusuario creado exitosamente!
✅ Build completed successfully!
```

---

### **Paso 4: Verificar el Superusuario** ✅

Una vez que el deployment termine:

1. Ve a: `https://korebase-erp.onrender.com/admin`
2. Inicia sesión con:
   - **Usuario**: `admin` (o el que configuraste)
   - **Contraseña**: La que configuraste en las variables de entorno

---

## 🎯 **VENTAJAS DE ESTA SOLUCIÓN**

✅ **Gratis** - No requiere Shell de pago  
✅ **Automático** - Se crea en cada deployment  
✅ **Seguro** - Usa variables de entorno  
✅ **Idempotente** - No crea duplicados  
✅ **Reproducible** - Funciona en cualquier entorno  

---

## 🔄 **ALTERNATIVA 2: Usar Django Admin Localmente**

Si prefieres crear el superusuario desde tu máquina local:

### **Opción A: Conectarse a Neon.tech Directamente**

1. **Copia** la `DATABASE_URL` de Render
2. **Pégala** en tu `.env` local (temporalmente)
3. **Ejecuta**:
   ```bash
   python manage.py createsuperuser
   ```
4. **Restaura** tu `.env` local

### **Opción B: Crear Localmente y Exportar**

1. **Crea** el superusuario localmente:
   ```bash
   python manage.py createsuperuser
   ```
2. **Exporta** el usuario:
   ```bash
   python manage.py dumpdata auth.User --indent 2 > superuser.json
   ```
3. **Sube** el archivo al servidor (requiere acceso SSH o Shell)

---

## 🔄 **ALTERNATIVA 3: Crear Vista de Registro Temporal**

Crear una vista temporal para registrar el primer admin:

### **Paso 1: Crear vista temporal**

```python
# core/views.py
from django.contrib.auth.models import User
from django.http import JsonResponse
import os

def create_first_admin(request):
    # Solo permitir en DEBUG o con token secreto
    secret = request.GET.get('secret')
    expected_secret = os.environ.get('ADMIN_CREATION_SECRET')
    
    if secret != expected_secret:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if User.objects.filter(username='admin').exists():
        return JsonResponse({'message': 'Admin already exists'})
    
    User.objects.create_superuser(
        username='admin',
        email='admin@korebase.com',
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    )
    
    return JsonResponse({'message': 'Admin created successfully'})
```

### **Paso 2: Agregar URL temporal**

```python
# core/urls.py
urlpatterns = [
    # ... otras URLs
    path('create-first-admin/', views.create_first_admin, name='create_first_admin'),
]
```

### **Paso 3: Visitar la URL**

```
https://korebase-erp.onrender.com/core/create-first-admin/?secret=TU_TOKEN_SECRETO
```

### **Paso 4: Eliminar la vista después de usarla**

⚠️ **IMPORTANTE**: Elimina esta vista después de crear el admin.

---

## 📊 **COMPARACIÓN DE ALTERNATIVAS**

| Alternativa | Dificultad | Seguridad | Costo | Recomendada |
|-------------|-----------|-----------|-------|-------------|
| **1. Build Script** | ⭐⭐ Fácil | 🔒🔒🔒 Alta | 💰 Gratis | ✅ **SÍ** |
| **2. Conexión Local** | ⭐⭐⭐ Media | 🔒🔒 Media | 💰 Gratis | ⚠️ Temporal |
| **3. Vista Temporal** | ⭐⭐⭐⭐ Difícil | 🔒 Baja | 💰 Gratis | ❌ No |

---

## 🎯 **RECOMENDACIÓN FINAL**

**Usa la ALTERNATIVA 1** (Build Script) porque:

1. ✅ Es **gratis**
2. ✅ Es **segura** (usa variables de entorno)
3. ✅ Es **automática** (no requiere intervención manual)
4. ✅ Es **reproducible** (funciona en cada deployment)
5. ✅ Es **profesional** (buena práctica de DevOps)

---

## 📝 **CHECKLIST**

- [ ] Crear `create_superuser.py`
- [ ] Actualizar `build.sh`
- [ ] Agregar variables de entorno en Render:
  - [ ] `DJANGO_SUPERUSER_USERNAME`
  - [ ] `DJANGO_SUPERUSER_EMAIL`
  - [ ] `DJANGO_SUPERUSER_PASSWORD`
- [ ] Hacer commit y push
- [ ] Esperar re-deployment
- [ ] Verificar login en `/admin`

---

## 🔐 **SEGURIDAD**

### **Contraseñas Recomendadas**

❌ **NO uses**:
- `admin123`
- `password`
- `12345678`

✅ **USA**:
- `KoreBase2026!Secure`
- `UPY_Admin_2026!`
- `ErpSecure@2026`

### **Después del Primer Login**

1. Cambia la contraseña desde el admin de Django
2. Crea usuarios adicionales con permisos limitados
3. Considera eliminar o deshabilitar el usuario `admin` después de crear otros admins

---

**Fecha**: 2026-01-29  
**Método Recomendado**: Alternativa 1 (Build Script)  
**Estado**: ✅ Archivos listos - Pendiente configurar variables de entorno

---

## 🚀 **PRÓXIMOS PASOS**

1. **Ahora**: Agregar variables de entorno en Render
2. **Luego**: Hacer commit y push
3. **Esperar**: 3-5 minutos (re-deployment)
4. **Verificar**: Login en `/admin`

**¿Listo para continuar?** 🎯
