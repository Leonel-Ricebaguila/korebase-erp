# 🚀 Guía de Despliegue - Render.com + Neon.tech + Cloudinary

## ✅ Compatibilidad con Arquitectura Frontend Modular

La arquitectura frontend modular implementada es **100% compatible** con el stack de producción:

- ✅ **Render.com**: Servicio web con WhiteNoise para archivos estáticos
- ✅ **Neon.tech**: Base de datos PostgreSQL serverless
- ✅ **Cloudinary**: Almacenamiento de archivos multimedia (imágenes, documentos)
- ✅ **Django Templates**: Renderizado del lado del servidor (SSR)

**IMPORTANTE**: La separación frontend/backend NO afecta el despliegue. Los templates se renderizan en el servidor de Render.com, los archivos estáticos (CSS/JS) se sirven con WhiteNoise, y las imágenes se almacenan en Cloudinary.

---

## 📊 Arquitectura en Producción

```
┌─────────────────────────────────────────────────────────────┐
│                      USUARIO (Navegador)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    RENDER.COM (Web Service)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Django Application (Python)                          │  │
│  │  ├── Views (Backend Logic) ✅ NO CAMBIOS             │  │
│  │  ├── Templates (Frontend HTML) ✅ MODULAR             │  │
│  │  └── Components (Reutilizables) ✅ NUEVO              │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  WhiteNoise (Static Files Middleware)                │  │
│  │  ├── CSS (design-system.css, etc.) ✅ COMPRIMIDO     │  │
│  │  ├── JavaScript (app.js, etc.) ✅ COMPRIMIDO         │  │
│  │  └── Fonts, Icons ✅ CACHEADOS                        │  │
│  └───────────────────────────────────────────────────────┘  │
└────────┬──────────────────────────────┬─────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│   NEON.TECH          │    │   CLOUDINARY.COM             │
│   PostgreSQL DB      │    │   Media Storage              │
│   ├── Users          │    │   ├── Product Images         │
│   ├── Products       │    │   ├── User Avatars           │
│   ├── Orders         │    │   └── Documents              │
│   └── Invoices       │    └──────────────────────────────┘
└──────────────────────┘
```

---

## 🔧 Configuración Actual (Ya Implementada)

### 1. **`settings.py`** ✅

```python
# Static Files - WhiteNoise
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files - Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Database - Neon.tech
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Templates - Modular
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],  # ✅ Layouts y componentes globales
    'APP_DIRS': True,  # ✅ Templates por módulo
}]

# Render.com
ALLOWED_HOSTS = ['korebase.onrender.com', '.onrender.com', 'localhost']
CSRF_TRUSTED_ORIGINS = ['https://korebase.onrender.com', 'https://*.onrender.com']
```

### 2. **`requirements.txt`** ✅

```
Django>=5.0
psycopg2-binary              # PostgreSQL (Neon.tech)
dj-database-url              # Parse DATABASE_URL
whitenoise                   # Servir archivos estáticos
cloudinary                   # SDK de Cloudinary
django-cloudinary-storage    # ✅ AGREGADO - Storage backend
django-htmx                  # Interactividad
gunicorn                     # WSGI server (Render.com)
python-dotenv                # Variables de entorno
pillow                       # Procesamiento de imágenes
```

### 3. **`build.sh`** ✅

```bash
#!/usr/bin/env bash
set -o errexit

echo "🚀 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input  # ✅ CSS/JS a staticfiles/

echo "🗄️  Running database migrations..."
python manage.py migrate  # ✅ Migraciones a Neon.tech

echo "✅ Build completed successfully!"
```

---

## 🎨 Cómo Funciona el Frontend Modular en Producción

### **Desarrollo Local (Windows)**

```
korebase-django/
├── static/                          # Archivos fuente
│   ├── css/design-system.css       # ✅ Variables CSS
│   └── js/app.js                   # ✅ JavaScript
├── templates/
│   ├── layouts/base.html           # ✅ Layout modular
│   └── components/                 # ✅ Componentes
└── [modulo]/templates/             # ✅ Vistas por módulo
```

### **Producción (Render.com)**

```
Render.com Container:
├── staticfiles/                     # ✅ Generado por collectstatic
│   ├── css/design-system.abc123.css  # Comprimido + hash
│   └── js/app.def456.js              # Comprimido + hash
├── templates/                       # ✅ Mismo código
│   ├── layouts/base.html
│   └── components/
└── [modulo]/templates/
```

**Flujo de Renderizado:**

1. **Usuario visita** `https://korebase.onrender.com/dashboard`
2. **Django (Render.com)** ejecuta `dashboard_view(request)`
3. **Vista retorna** datos (usuarios, métricas, etc.)
4. **Template engine** renderiza `dashboard.html` con componentes
5. **HTML final** se envía al navegador
6. **Navegador carga**:
   - CSS desde WhiteNoise (Render.com)
   - JS desde WhiteNoise (Render.com)
   - Imágenes desde Cloudinary

---

## 📋 Checklist de Despliegue

### **Paso 1: Configurar Variables de Entorno en Render.com**

En el dashboard de Render.com, agrega estas variables:

```env
# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=False
PYTHON_VERSION=3.11.9

# Database (Neon.tech)
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/korebase?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

**Obtener DATABASE_URL de Neon.tech:**
1. Ve a tu proyecto en Neon.tech
2. Copia la "Connection String" (formato PostgreSQL)
3. Pégala en Render.com como `DATABASE_URL`

**Obtener credenciales de Cloudinary:**
1. Ve a tu dashboard de Cloudinary
2. Copia: Cloud Name, API Key, API Secret
3. Agrégalos en Render.com

### **Paso 2: Configurar Render.com**

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn korebase.wsgi:application
```

**Environment:**
- Python Version: `3.11.9`
- Region: `Oregon (US West)` o el más cercano

### **Paso 3: Desplegar**

```bash
# 1. Commit de cambios
git add .
git commit -m "chore: preparar para despliegue en Render.com"
git push origin main

# 2. Render.com detectará el push y desplegará automáticamente
```

### **Paso 4: Verificar Despliegue**

1. **Logs de Build**: Verifica que `collectstatic` se ejecute sin errores
2. **Logs de Runtime**: Verifica que la app inicie correctamente
3. **Prueba la URL**: `https://korebase.onrender.com`
4. **Verifica archivos estáticos**: CSS y JS deben cargarse
5. **Prueba subida de imágenes**: Deben guardarse en Cloudinary

---

## 🔍 Verificación de Archivos Estáticos

### **En Desarrollo (Local)**

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/design-system.css' %}">
<!-- Resultado: http://localhost:8000/static/css/design-system.css -->
```

### **En Producción (Render.com)**

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/design-system.css' %}">
<!-- Resultado: https://korebase.onrender.com/static/css/design-system.abc123.css -->
<!-- WhiteNoise agrega hash para cache busting -->
```

**Ventajas de WhiteNoise:**
- ✅ Compresión Gzip/Brotli automática
- ✅ Cache headers optimizados
- ✅ Hash en nombres de archivo (cache busting)
- ✅ No requiere CDN adicional

---

## 🖼️ Verificación de Archivos Multimedia

### **Subir Imagen desde el Admin**

```python
# models.py
from cloudinary.models import CloudinaryField

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = CloudinaryField('image')  # ✅ Se sube a Cloudinary
```

**En producción:**
1. Usuario sube imagen en `/admin/logistica/product/add/`
2. Django procesa el upload
3. `cloudinary_storage` sube a Cloudinary
4. URL guardada: `https://res.cloudinary.com/tu-cloud/image/upload/v123/product.jpg`
5. Imagen se muestra desde Cloudinary (no desde Render.com)

---

## ⚡ Optimizaciones para Producción

### 1. **Comprimir CSS/JS Adicional**

Si agregas CSS/JS personalizado, asegúrate de que esté en `static/`:

```
static/
├── css/
│   ├── design-system.css      # ✅ Se comprime
│   └── modules/
│       └── logistica.css      # ✅ Se comprime
└── js/
    ├── app.js                 # ✅ Se comprime
    └── components/
        └── sidebar.js         # ✅ Se comprime
```

### 2. **Lazy Loading de Imágenes**

```django
{# En tus templates #}
<img src="{{ product.image.url }}" 
     loading="lazy"
     alt="{{ product.name }}">
```

### 3. **CDN de Font Awesome (Ya configurado)**

```html
<!-- En layouts/base.html -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

### 4. **Caché de Templates (Opcional)**

Para mejorar performance en producción:

```python
# settings.py (solo si DEBUG=False)
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
```

---

## 🐛 Solución de Problemas

### **Problema: CSS/JS no se cargan**

**Solución:**
```bash
# En Render.com, verifica los logs de build
# Debe aparecer:
# "📦 Collecting static files..."
# "X static files copied to '/opt/render/project/src/staticfiles'"
```

Si no aparece, verifica:
1. `STATICFILES_DIRS = [BASE_DIR / 'static']` en `settings.py`
2. Archivos existen en `static/css/` y `static/js/`
3. `build.sh` tiene permisos de ejecución: `chmod +x build.sh`

### **Problema: Imágenes no se suben a Cloudinary**

**Solución:**
1. Verifica variables de entorno en Render.com
2. Verifica que `cloudinary_storage` esté en `INSTALLED_APPS`
3. Verifica que `DEFAULT_FILE_STORAGE` esté configurado
4. Revisa logs de Render.com para errores de Cloudinary

### **Problema: Error de conexión a Neon.tech**

**Solución:**
1. Verifica que `DATABASE_URL` incluya `?sslmode=require`
2. Verifica que la IP de Render.com esté permitida en Neon.tech
3. Verifica que `psycopg2-binary` esté en `requirements.txt`

---

## 📊 Monitoreo en Producción

### **Logs de Render.com**

```bash
# Ver logs en tiempo real desde el dashboard de Render.com
# O desde la CLI:
render logs -s korebase
```

### **Métricas a Monitorear**

1. **Tiempo de respuesta**: < 500ms ideal
2. **Uso de memoria**: < 512MB (plan gratuito)
3. **Errores 500**: Deben ser 0
4. **Tiempo de build**: < 5 minutos

---

## ✅ Checklist Final

Antes de desplegar a producción:

- [x] `requirements.txt` actualizado con `django-cloudinary-storage`
- [x] `cloudinary_storage` en `INSTALLED_APPS`
- [x] Variables de entorno configuradas en Render.com
- [x] `build.sh` con permisos de ejecución
- [x] `DEBUG=False` en producción
- [x] `ALLOWED_HOSTS` incluye dominio de Render
- [x] `CSRF_TRUSTED_ORIGINS` configurado
- [x] Archivos estáticos en `static/`
- [x] Templates modulares funcionando localmente
- [ ] Prueba local con `DEBUG=False` y `collectstatic`
- [ ] Deploy a Render.com
- [ ] Verificar logs de build
- [ ] Verificar que la app cargue
- [ ] Probar login
- [ ] Probar subida de imágenes

---

## 🎉 Resultado Final

**URL de Producción**: `https://korebase.onrender.com`

**Stack Completo:**
- ✅ **Frontend**: Templates modulares + Componentes reutilizables
- ✅ **Backend**: Django views (sin cambios)
- ✅ **Archivos Estáticos**: WhiteNoise (CSS, JS, fonts)
- ✅ **Archivos Multimedia**: Cloudinary (imágenes, documentos)
- ✅ **Base de Datos**: Neon.tech (PostgreSQL)
- ✅ **Hosting**: Render.com (Web Service)

**Ventajas:**
- ✅ Separación frontend/backend mantenida
- ✅ Sin cambios en el código de producción
- ✅ Componentes funcionan igual en dev y prod
- ✅ Archivos estáticos optimizados automáticamente
- ✅ Escalable y mantenible

---

**¡Listo para desplegar!** 🚀

Para desplegar, simplemente haz push a tu repositorio y Render.com se encargará del resto.
