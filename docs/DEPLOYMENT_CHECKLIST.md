# ✅ Checklist Interactivo de Deployment

## 🎯 Objetivo
Desplegar KoreBase ERP en producción con:
- 🌐 Render.com (Hosting)
- 🗄️ Neon.tech (PostgreSQL)
- 📁 Cloudinary (Archivos multimedia)

---

## FASE 1: Neon.tech (Base de Datos) ⏳

### Paso 1.1: Crear Cuenta
- [ ] Abrir: https://neon.tech
- [ ] Clic en "Sign Up"
- [ ] Registrarse con GitHub o Email
- [ ] Verificar email (si es necesario)

### Paso 1.2: Crear Proyecto
- [ ] Clic en "Create a project"
- [ ] Nombre del proyecto: `korebase-erp`
- [ ] Región: `US East (Ohio)` o la más cercana
- [ ] PostgreSQL version: `16`
- [ ] Clic en "Create project"

### Paso 1.3: Copiar Connection String
- [ ] En el dashboard, buscar "Connection Details"
- [ ] Copiar la "Connection string" completa
- [ ] Debe verse así:
  ```
  postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/korebase?sslmode=require
  ```
- [ ] **GUARDAR EN UN LUGAR SEGURO** (la necesitarás después)

**⚠️ IMPORTANTE**: Asegúrate de que termine con `?sslmode=require`

---

## FASE 2: Cloudinary (Almacenamiento) ⏳

### Paso 2.1: Crear Cuenta
- [ ] Abrir: https://cloudinary.com
- [ ] Clic en "Sign Up Free"
- [ ] Registrarse con email
- [ ] Verificar email

### Paso 2.2: Obtener Credenciales
- [ ] Ir al Dashboard
- [ ] Copiar las siguientes credenciales:
  - [ ] **Cloud Name**: `dxxxxxxxxx`
  - [ ] **API Key**: `123456789012345`
  - [ ] **API Secret**: `xxxxxxxxxxxxxxxxxxxx` (clic en el ojo para revelar)
- [ ] **GUARDAR EN UN LUGAR SEGURO**

---

## FASE 3: Generar SECRET_KEY ⏳

### Opción A: Desde tu Terminal Local

```powershell
# Activa el entorno virtual
.\venv\Scripts\Activate

# Genera la clave
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

- [ ] Ejecutar el comando
- [ ] Copiar la clave generada
- [ ] **GUARDAR EN UN LUGAR SEGURO**

### Opción B: Generador Online
- [ ] Ir a: https://djecrety.ir/
- [ ] Copiar la clave generada
- [ ] **GUARDAR EN UN LUGAR SEGURO**

---

## FASE 4: Render.com (Hosting) ⏳

### Paso 4.1: Crear Cuenta
- [ ] Abrir: https://render.com
- [ ] Clic en "Get Started"
- [ ] Registrarse con GitHub (recomendado)
- [ ] Autorizar a Render para acceder a tus repositorios

### Paso 4.2: Crear Web Service
- [ ] En el dashboard, clic en "New +" → "Web Service"
- [ ] Buscar y seleccionar: `Leonel-Ricebaguila/korebase-erp`
  - Si no aparece, clic en "Configure account" y autorizar
- [ ] Clic en "Connect"

### Paso 4.3: Configuración Básica

Completa los siguientes campos:

- [ ] **Name**: `korebase-erp`
- [ ] **Region**: `Oregon (US West)` o el más cercano
- [ ] **Branch**: `main`
- [ ] **Root Directory**: (dejar vacío)
- [ ] **Runtime**: `Python 3`
- [ ] **Build Command**: `./build.sh`
- [ ] **Start Command**: `gunicorn korebase.wsgi:application`
- [ ] **Plan**: `Free` (para pruebas) o `Starter` ($7/mes)

### Paso 4.4: Configurar Variables de Entorno

**MUY IMPORTANTE**: Antes de crear el servicio, configura las variables.

- [ ] Clic en "Advanced"
- [ ] Agregar las siguientes variables (una por una):

#### Variable 1: SECRET_KEY
- [ ] Key: `SECRET_KEY`
- [ ] Value: (pegar la clave que generaste en FASE 3)

#### Variable 2: DEBUG
- [ ] Key: `DEBUG`
- [ ] Value: `False`

#### Variable 3: PYTHON_VERSION
- [ ] Key: `PYTHON_VERSION`
- [ ] Value: `3.11.9`

#### Variable 4: DATABASE_URL
- [ ] Key: `DATABASE_URL`
- [ ] Value: (pegar la connection string de Neon.tech de FASE 1)

#### Variable 5: CLOUDINARY_CLOUD_NAME
- [ ] Key: `CLOUDINARY_CLOUD_NAME`
- [ ] Value: (pegar tu Cloud Name de FASE 2)

#### Variable 6: CLOUDINARY_API_KEY
- [ ] Key: `CLOUDINARY_API_KEY`
- [ ] Value: (pegar tu API Key de FASE 2)

#### Variable 7: CLOUDINARY_API_SECRET
- [ ] Key: `CLOUDINARY_API_SECRET`
- [ ] Value: (pegar tu API Secret de FASE 2)

### Paso 4.5: Crear el Servicio
- [ ] Verificar que TODAS las variables estén configuradas
- [ ] Clic en "Create Web Service"
- [ ] Esperar 3-5 minutos mientras Render:
  - [ ] Clona el repositorio
  - [ ] Instala dependencias
  - [ ] Recopila archivos estáticos
  - [ ] Ejecuta migraciones
  - [ ] Inicia el servidor

---

## FASE 5: Verificar Deployment ⏳

### Paso 5.1: Monitorear Logs
- [ ] En Render, ir a la pestaña "Logs"
- [ ] Verificar que aparezcan estos mensajes:
  - [ ] `🚀 Installing dependencies...`
  - [ ] `📦 Collecting static files...`
  - [ ] `🗄️  Running database migrations...`
  - [ ] `✅ Build completed successfully!`

### Paso 5.2: Verificar Estado
- [ ] Esperar a que el estado cambie a "Live" (verde)
- [ ] Copiar la URL de tu aplicación:
  ```
  https://korebase-erp.onrender.com
  ```

### Paso 5.3: Visitar la Aplicación
- [ ] Abrir la URL en el navegador
- [ ] Deberías ver la página de login

---

## FASE 6: Crear Superusuario ⏳

### Paso 6.1: Acceder al Shell de Render
- [ ] En Render, ir a tu servicio
- [ ] Clic en "Shell" (en el menú lateral)
- [ ] Esperar a que se abra la terminal

### Paso 6.2: Crear Superusuario
- [ ] En el shell, ejecutar:
  ```bash
  python manage.py createsuperuser
  ```
- [ ] Ingresar los datos:
  - [ ] **Username**: `admin`
  - [ ] **Email**: `tu-email@example.com`
  - [ ] **Password**: (una contraseña SEGURA, NO `admin123`)
  - [ ] **Password (again)**: (repetir la contraseña)
  - [ ] **Employee ID**: `EMP-001` (si lo pide)

### Paso 6.3: Verificar Login
- [ ] Ir a: `https://korebase-erp.onrender.com/admin`
- [ ] Iniciar sesión con las credenciales del superusuario
- [ ] Deberías ver el panel de administración de Django

---

## FASE 7: Verificaciones Finales ⏳

### Verificación 1: Archivos Estáticos
- [ ] Abrir la aplicación
- [ ] Presionar F12 (DevTools)
- [ ] Ir a la pestaña "Network"
- [ ] Recargar la página
- [ ] Verificar que los archivos CSS/JS se carguen (Status 200):
  - [ ] `static/css/design-system.css`
  - [ ] `static/js/app.js`

### Verificación 2: Base de Datos
- [ ] En el admin, ir a "Users"
- [ ] Deberías ver tu superusuario
- [ ] Intentar crear un usuario de prueba
- [ ] Verificar que se guarde correctamente

### Verificación 3: Cloudinary (Opcional)
- [ ] En el admin, buscar un modelo con imágenes
- [ ] Intentar subir una imagen de prueba
- [ ] Ir al dashboard de Cloudinary
- [ ] Verificar que la imagen aparezca en "Media Library"

---

## 🎉 ¡DEPLOYMENT COMPLETADO!

Si todas las verificaciones pasaron, tu aplicación está funcionando en producción:

**URL de Producción**: `https://korebase-erp.onrender.com`

**Credenciales de Admin**:
- Usuario: `admin` (o el que creaste)
- Contraseña: (la que configuraste)

---

## 📊 Resumen de Credenciales

**Guarda esta información en un lugar seguro:**

```
=== NEON.TECH ===
DATABASE_URL: postgresql://...

=== CLOUDINARY ===
CLOUDINARY_CLOUD_NAME: dxxxxxxxxx
CLOUDINARY_API_KEY: 123456789012345
CLOUDINARY_API_SECRET: xxxxxxxxxxxxxxxxxxxx

=== DJANGO ===
SECRET_KEY: django-insecure-...

=== ADMIN ===
Username: admin
Password: [tu contraseña segura]
Email: [tu email]
```

---

## 🐛 Si Algo Sale Mal

### Error en Build
- [ ] Verificar que todas las variables de entorno estén configuradas
- [ ] Verificar los logs en Render
- [ ] Verificar que `build.sh` tenga permisos de ejecución

### Error en Migraciones
- [ ] Verificar que `DATABASE_URL` sea correcta
- [ ] Verificar que termine con `?sslmode=require`
- [ ] Copiar nuevamente la connection string de Neon.tech

### Error 500
- [ ] Ir a los logs en Render
- [ ] Buscar el error específico
- [ ] Verificar que `DEBUG=False`
- [ ] Verificar que todas las variables estén configuradas

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render (pestaña "Logs")
2. Consulta: `PRODUCTION_DEPLOYMENT.md` para más detalles
3. Verifica que todas las variables de entorno estén correctas

---

**¡Éxito con tu deployment!** 🚀
