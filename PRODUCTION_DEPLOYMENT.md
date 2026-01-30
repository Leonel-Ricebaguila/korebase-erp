# 🚀 Guía de Deployment Paso a Paso - Producción

## 📋 Stack de Producción

- 🌐 **Render.com** - Hosting del servidor Django
- 🗄️ **Neon.tech** - Base de datos PostgreSQL
- 📁 **Cloudinary** - Almacenamiento de archivos multimedia

---

## ✅ Pre-requisitos

Antes de empezar, necesitas tener cuentas en:

1. ✅ **GitHub** - Ya tienes el repositorio: `Leonel-Ricebaguila/korebase-erp`
2. ⏳ **Render.com** - Crear cuenta gratuita
3. ⏳ **Neon.tech** - Crear cuenta gratuita
4. ⏳ **Cloudinary** - Crear cuenta gratuita

---

# PASO 1: Configurar Neon.tech (Base de Datos PostgreSQL)

## 1.1 Crear Cuenta en Neon.tech

1. Ve a: **https://neon.tech**
2. Haz clic en **"Sign Up"**
3. Regístrate con GitHub (recomendado) o email
4. Verifica tu email si es necesario

## 1.2 Crear Proyecto

1. Una vez dentro, haz clic en **"Create a project"**
2. Configura:
   - **Project name**: `korebase-erp`
   - **Region**: `US East (Ohio)` o el más cercano
   - **PostgreSQL version**: `16` (la más reciente)
3. Haz clic en **"Create project"**

## 1.3 Obtener Connection String

1. En el dashboard del proyecto, verás **"Connection Details"**
2. Copia la **"Connection string"** completa
3. Debería verse así:
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/korebase?sslmode=require
   ```
4. **GUARDA ESTA URL** - La necesitarás para Render.com

### ⚠️ IMPORTANTE:
- Asegúrate de que termine con `?sslmode=require`
- Si no lo tiene, agrégalo manualmente

---

# PASO 2: Configurar Cloudinary (Almacenamiento de Archivos)

## 2.1 Crear Cuenta en Cloudinary

1. Ve a: **https://cloudinary.com**
2. Haz clic en **"Sign Up Free"**
3. Regístrate con email
4. Verifica tu email

## 2.2 Obtener Credenciales

1. Una vez dentro, ve al **Dashboard**
2. Verás tus credenciales:
   - **Cloud Name**: `dxxxxxxxxx`
   - **API Key**: `123456789012345`
   - **API Secret**: `xxxxxxxxxxxxxxxxxxxx`
3. **GUARDA ESTAS CREDENCIALES** - Las necesitarás para Render.com

### 📝 Nota:
- Puedes hacer clic en el ícono del ojo para revelar el API Secret
- Copia y pega en un lugar seguro (no las compartas públicamente)

---

# PASO 3: Configurar Render.com (Hosting)

## 3.1 Crear Cuenta en Render.com

1. Ve a: **https://render.com**
2. Haz clic en **"Get Started"**
3. Regístrate con GitHub (recomendado)
4. Autoriza a Render para acceder a tus repositorios

## 3.2 Crear Web Service

1. En el dashboard, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio:
   - Si no aparece, haz clic en **"Configure account"**
   - Autoriza acceso a `Leonel-Ricebaguila/korebase-erp`
3. Selecciona el repositorio: **`korebase-erp`**
4. Haz clic en **"Connect"**

## 3.3 Configurar el Web Service

### **Configuración Básica:**

| Campo | Valor |
|-------|-------|
| **Name** | `korebase-erp` |
| **Region** | `Oregon (US West)` o el más cercano |
| **Branch** | `main` |
| **Root Directory** | (dejar vacío) |
| **Runtime** | `Python 3` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn korebase.wsgi:application` |

### **Plan:**
- Selecciona: **"Free"** (para pruebas)
- O **"Starter"** ($7/mes) para mejor rendimiento

## 3.4 Configurar Variables de Entorno

**MUY IMPORTANTE**: Antes de hacer clic en "Create Web Service", configura las variables de entorno.

Haz clic en **"Advanced"** y agrega las siguientes variables:

### **Variables Requeridas:**

```env
# Django
SECRET_KEY=<GENERA_UNA_CLAVE_SEGURA>
DEBUG=False
PYTHON_VERSION=3.11.9

# Database (Neon.tech)
DATABASE_URL=<TU_CONNECTION_STRING_DE_NEON>

# Cloudinary
CLOUDINARY_CLOUD_NAME=<TU_CLOUD_NAME>
CLOUDINARY_API_KEY=<TU_API_KEY>
CLOUDINARY_API_SECRET=<TU_API_SECRET>
```

### **Cómo Generar SECRET_KEY:**

Opción 1 - En tu terminal local:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Opción 2 - Usar un generador online:
- https://djecrety.ir/

**Copia la clave generada y pégala en SECRET_KEY**

### **Ejemplo de Variables Configuradas:**

```env
SECRET_KEY=django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
DEBUG=False
PYTHON_VERSION=3.11.9
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/korebase?sslmode=require
CLOUDINARY_CLOUD_NAME=dxxxxxxxxx
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=xxxxxxxxxxxxxxxxxxxx
```

## 3.5 Crear el Servicio

1. Verifica que todas las variables estén configuradas
2. Haz clic en **"Create Web Service"**
3. Render comenzará a:
   - ✅ Clonar el repositorio
   - ✅ Instalar dependencias (`pip install -r requirements.txt`)
   - ✅ Recopilar archivos estáticos (`collectstatic`)
   - ✅ Ejecutar migraciones (`migrate`)
   - ✅ Iniciar el servidor (`gunicorn`)

### **Tiempo estimado:** 3-5 minutos

---

# PASO 4: Monitorear el Deployment

## 4.1 Ver Logs de Build

1. En Render, verás la pestaña **"Logs"**
2. Observa el proceso de build:

```
🚀 Installing dependencies...
Collecting Django>=5.0
...
Successfully installed Django-5.0.1 ...

📦 Collecting static files...
X static files copied to '/opt/render/project/src/staticfiles'

🗄️  Running database migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, logistica, produccion, financiero
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...

✅ Build completed successfully!
```

## 4.2 Verificar que el Servicio Esté Activo

1. Espera a que el estado cambie a **"Live"** (verde)
2. Verás la URL de tu aplicación:
   ```
   https://korebase-erp.onrender.com
   ```

---

# PASO 5: Configuración Post-Deployment

## 5.1 Crear Superusuario

**IMPORTANTE**: Necesitas crear un superusuario para acceder al admin.

### **Opción A: Desde Render Shell (Recomendado)**

1. En Render, ve a tu servicio
2. Haz clic en **"Shell"** (en el menú lateral)
3. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```
4. Ingresa:
   - **Username**: `admin`
   - **Email**: `tu-email@example.com`
   - **Password**: (una contraseña segura, NO `admin123`)
   - **Password (again)**: (repite la contraseña)

### **Opción B: Crear Script de Inicialización**

Si prefieres automatizar, puedes crear un script, pero por ahora usa la Opción A.

## 5.2 Verificar la Aplicación

1. Visita tu URL: `https://korebase-erp.onrender.com`
2. Deberías ver la página de login
3. Intenta acceder al admin: `https://korebase-erp.onrender.com/admin`
4. Inicia sesión con el superusuario que creaste

---

# PASO 6: Verificaciones Finales

## 6.1 Verificar Archivos Estáticos

1. Inspecciona la página (F12)
2. Ve a la pestaña **"Network"**
3. Recarga la página
4. Verifica que los archivos CSS/JS se carguen correctamente:
   - `static/css/design-system.css` → Status 200
   - `static/js/app.js` → Status 200

## 6.2 Verificar Base de Datos

1. Accede al admin: `/admin`
2. Ve a **"Users"**
3. Deberías ver tu superusuario
4. Intenta crear un usuario de prueba

## 6.3 Verificar Cloudinary (Opcional)

1. En el admin, ve a un modelo que tenga imágenes
2. Intenta subir una imagen
3. Ve al dashboard de Cloudinary
4. Deberías ver la imagen subida en **"Media Library"**

---

# PASO 7: Configuración de Dominio (Opcional)

Si tienes un dominio personalizado:

1. En Render, ve a **"Settings"** → **"Custom Domain"**
2. Agrega tu dominio: `www.tudominio.com`
3. Configura los DNS según las instrucciones de Render
4. Render generará automáticamente un certificado SSL

---

# 🐛 Solución de Problemas

## Problema 1: Build Falla

**Error**: `ERROR: Could not find a version that satisfies the requirement...`

**Solución**:
1. Verifica que `requirements.txt` esté correcto
2. Verifica que `PYTHON_VERSION=3.11.9` esté configurado

## Problema 2: Migraciones Fallan

**Error**: `django.db.utils.OperationalError: FATAL: password authentication failed`

**Solución**:
1. Verifica que `DATABASE_URL` esté correcta
2. Verifica que termine con `?sslmode=require`
3. Copia nuevamente la connection string de Neon.tech

## Problema 3: Archivos Estáticos No Cargan

**Error**: CSS/JS no se ven en la página

**Solución**:
1. Verifica los logs de build: debe aparecer `collectstatic`
2. Verifica que `STATICFILES_STORAGE` esté configurado en `settings.py`
3. Verifica que `whitenoise` esté en `MIDDLEWARE`

## Problema 4: Error 500

**Error**: Internal Server Error

**Solución**:
1. Ve a los logs en Render: **"Logs"** tab
2. Busca el error específico
3. Verifica que todas las variables de entorno estén configuradas
4. Verifica que `DEBUG=False` esté configurado

## Problema 5: No Puedo Crear Superusuario

**Error**: `CommandError: This field cannot be blank`

**Solución**:
1. Asegúrate de que el modelo `CustomUser` tenga `employee_id` opcional
2. O proporciona un `employee_id` al crear el superusuario

---

# ✅ Checklist de Deployment

- [ ] Cuenta en Neon.tech creada
- [ ] Base de datos PostgreSQL creada
- [ ] Connection string copiada
- [ ] Cuenta en Cloudinary creada
- [ ] Credenciales de Cloudinary copiadas
- [ ] Cuenta en Render.com creada
- [ ] Repositorio conectado
- [ ] Variables de entorno configuradas
- [ ] SECRET_KEY generada
- [ ] Web Service creado
- [ ] Build completado exitosamente
- [ ] Servicio en estado "Live"
- [ ] Superusuario creado
- [ ] Login funciona
- [ ] Admin accesible
- [ ] Archivos estáticos cargan
- [ ] Base de datos funciona

---

# 🎉 ¡Deployment Completado!

Tu aplicación debería estar funcionando en:

```
https://korebase-erp.onrender.com
```

**Credenciales de Admin:**
- Usuario: `admin` (o el que creaste)
- Contraseña: (la que configuraste)

---

# 📊 Monitoreo Continuo

## Logs en Tiempo Real

En Render, ve a **"Logs"** para ver:
- Requests HTTP
- Errores de aplicación
- Queries a la base de datos

## Métricas

En Render, ve a **"Metrics"** para ver:
- CPU usage
- Memory usage
- Request count
- Response time

---

# 🔄 Actualizaciones Futuras

Cuando hagas cambios en el código:

```bash
# 1. Commit y push a GitHub
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main

# 2. Render detectará el push y redesplegará automáticamente
```

---

**¡Tu aplicación está en producción!** 🚀

Si tienes problemas, revisa la sección de **Solución de Problemas** o consulta los logs en Render.
