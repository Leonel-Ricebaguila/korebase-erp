# 🔐 CONFIGURACIÓN COMPLETA PARA RENDER.COM

## ✅ TODAS LAS CREDENCIALES LISTAS

---

## 📋 CONFIGURACIÓN DEL WEB SERVICE

### **Campos Básicos:**

| Campo | Valor |
|-------|-------|
| **Name** | `korebase-erp` |
| **Project** | `My project` |
| **Language** | `Python 3` |
| **Branch** | `main` |
| **Region** | `Virginia (US East)` |
| **Root Directory** | *(dejar vacío)* |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn korebase.wsgi:application` |
| **Instance Type** | `Free` |

---

## 🔑 VARIABLES DE ENTORNO (7 VARIABLES)

**COPIA Y PEGA EXACTAMENTE ESTAS VARIABLES EN RENDER.COM:**

### Variable 1: SECRET_KEY
```
Key:   SECRET_KEY
Value: evn*+)c*si7jb3!o_)%2!xhgu(mtroz8yv*5q$_7&i3bu(b@i*
```

### Variable 2: DEBUG
```
Key:   DEBUG
Value: False
```

### Variable 3: PYTHON_VERSION
```
Key:   PYTHON_VERSION
Value: 3.11.9
```

### Variable 4: DATABASE_URL
```
Key:   DATABASE_URL
Value: postgresql://neondb_owner:npg_zMfniT4c7IjR@ep-red-cell-ahuue57k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### Variable 5: CLOUDINARY_CLOUD_NAME
```
Key:   CLOUDINARY_CLOUD_NAME
Value: dwnvornf4
```

### Variable 6: CLOUDINARY_API_KEY
```
Key:   CLOUDINARY_API_KEY
Value: 566199747689974
```

### Variable 7: CLOUDINARY_API_SECRET
```
Key:   CLOUDINARY_API_SECRET
Value: qLQw1nIW_x-PTqC4js_BvODPhjY
```

---

## 📝 FORMATO PARA COPIAR/PEGAR RÁPIDO

Si Render.com permite pegar múltiples variables a la vez, usa este formato:

```env
SECRET_KEY=evn*+)c*si7jb3!o_)%2!xhgu(mtroz8yv*5q$_7&i3bu(b@i*
DEBUG=False
PYTHON_VERSION=3.11.9
DATABASE_URL=postgresql://neondb_owner:npg_zMfniT4c7IjR@ep-red-cell-ahuue57k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
CLOUDINARY_CLOUD_NAME=dwnvornf4
CLOUDINARY_API_KEY=566199747689974
CLOUDINARY_API_SECRET=qLQw1nIW_x-PTqC4js_BvODPhjY
```

---

## ✅ CHECKLIST FINAL

Antes de hacer clic en "Create Web Service":

- [x] Name: `korebase-erp`
- [x] Branch: `main`
- [x] Region: `Virginia (US East)`
- [x] Build Command: `./build.sh`
- [x] Start Command: `gunicorn korebase.wsgi:application`
- [x] Instance Type: `Free`
- [x] SECRET_KEY configurada
- [x] DEBUG configurada
- [x] PYTHON_VERSION configurada
- [x] DATABASE_URL configurada
- [x] CLOUDINARY_CLOUD_NAME configurada
- [x] CLOUDINARY_API_KEY configurada
- [x] CLOUDINARY_API_SECRET configurada

---

## 🚀 PASOS PARA DESPLEGAR

### 1. Configurar Variables de Entorno

En Render.com, en la sección **"Environment Variables"** o **"Advanced"**:

1. Haz clic en **"Add Environment Variable"**
2. Agrega cada variable **una por una** usando los valores de arriba
3. Verifica que las 7 variables estén agregadas

### 2. Crear el Servicio

1. Verifica que TODOS los campos estén correctos
2. Haz clic en **"Create Web Service"** (botón azul)
3. Render comenzará el deployment

### 3. Monitorear el Build (3-5 minutos)

Verás en los logs:

```
==> Cloning from https://github.com/Leonel-Ricebaguila/korebase-erp...
==> Running build command './build.sh'...

🚀 Installing dependencies...
Collecting Django>=5.0
...
Successfully installed Django-5.0.1 ...

📦 Collecting static files...
180 static files copied to '/opt/render/project/src/staticfiles'

🗄️  Running database migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, logistica, produccion, financiero
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  ...
  Applying core.0001_initial... OK
  Applying logistica.0001_initial... OK
  Applying produccion.0001_initial... OK
  Applying financiero.0001_initial... OK
  ...

✅ Build completed successfully!

==> Starting service with 'gunicorn korebase.wsgi:application'...
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 23
```

### 4. Verificar Estado

- Espera a que el estado cambie a **"Live"** (verde)
- Copia tu URL: `https://korebase-erp.onrender.com`

---

## 🎉 RESULTADO ESPERADO

Una vez que el deployment esté completo:

✅ **URL de Producción**: `https://korebase-erp.onrender.com`  
✅ **Base de Datos**: Conectada a Neon.tech  
✅ **Archivos Multimedia**: Conectados a Cloudinary  
✅ **Archivos Estáticos**: Servidos por WhiteNoise  
✅ **SSL/HTTPS**: Automático  

---

## 📊 SIGUIENTE PASO: CREAR SUPERUSUARIO

Una vez que el servicio esté **"Live"**:

1. En Render.com, ve a tu servicio `korebase-erp`
2. Haz clic en **"Shell"** (en el menú lateral)
3. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```
4. Ingresa:
   - **Username**: `admin`
   - **Email**: `tu-email@example.com`
   - **Password**: (una contraseña SEGURA)
   - **Password (again)**: (repetir)
   - **Employee ID**: `EMP-001` (si lo pide)

5. Visita: `https://korebase-erp.onrender.com/admin`
6. Inicia sesión con las credenciales

---

## 🐛 SI ALGO SALE MAL

### Error en Build:
- Revisa los logs en Render
- Busca líneas con "ERROR"
- Verifica que todas las variables estén configuradas

### Error de Base de Datos:
- Verifica que `DATABASE_URL` esté correcta
- Verifica que termine con `?sslmode=require`

### Error 500:
- Ve a los logs de runtime (no solo build)
- Busca el error específico
- Verifica que `DEBUG=False`

---

## ✅ CREDENCIALES GUARDADAS

**GUARDA ESTA INFORMACIÓN EN UN LUGAR SEGURO:**

```
=== NEON.TECH ===
DATABASE_URL: postgresql://neondb_owner:npg_zMfniT4c7IjR@ep-red-cell-ahuue57k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

=== CLOUDINARY ===
CLOUDINARY_CLOUD_NAME: dwnvornf4
CLOUDINARY_API_KEY: 566199747689974
CLOUDINARY_API_SECRET: qLQw1nIW_x-PTqC4js_BvODPhjY

=== DJANGO ===
SECRET_KEY: evn*+)c*si7jb3!o_)%2!xhgu(mtroz8yv*5q$_7&i3bu(b@i*

=== RENDER.COM ===
URL: https://korebase-erp.onrender.com
```

---

**¡TODO LISTO PARA DESPLEGAR!** 🚀

Ahora puedes ir a Render.com y crear el Web Service con esta configuración.
