# ✅ Configuración Correcta de Render.com - Web Service

## 📋 Formulario de Creación de Web Service

Basado en la interfaz actual de Render.com, aquí está la configuración **EXACTA** que debes usar:

---

## 🔧 Campos del Formulario

### **Source Code** ✅
- Ya debería estar seleccionado: `Leonel-Ricebaguila / korebase-erp`
- Si no aparece, haz clic en "Edit" y selecciona el repositorio

---

### **Name** (Requerido)
```
korebase-erp
```
- Este será el nombre de tu servicio
- También será parte de tu URL: `korebase-erp.onrender.com`

---

### **Project** (Opcional)
- **Opción 1**: Dejar en "My project" (recomendado para empezar)
- **Opción 2**: Crear un nuevo proyecto llamado "Production" si quieres organizar mejor

**Recomendación**: Deja "My project" por ahora

---

### **Language** (Requerido)
```
Python 3
```
- Debe estar seleccionado automáticamente
- Si no, selecciona "Python 3" del dropdown

---

### **Branch** (Requerido)
```
main
```
- Esta es la rama que se desplegará
- Cada push a `main` redesplegará automáticamente

---

### **Region** (Requerido)
```
Virginia (US East)
```

**Opciones disponibles**:
- `Virginia (US East)` - ✅ **RECOMENDADO** (más cercano a Neon.tech US East)
- `Oregon (US West)`
- `Frankfurt (EU Central)`
- `Singapore (Asia)`

**⚠️ IMPORTANTE**: Elige la misma región (o cercana) que tu base de datos de Neon.tech para menor latencia.

---

### **Root Directory** (Opcional)
```
(dejar vacío)
```
- No escribas nada aquí
- El código está en la raíz del repositorio

---

### **Build Command** (Requerido)
```
./build.sh
```

**Explicación**: Este comando:
1. Instala dependencias (`pip install -r requirements.txt`)
2. Recopila archivos estáticos (`collectstatic`)
3. Ejecuta migraciones (`migrate`)

**⚠️ IMPORTANTE**: Asegúrate de escribir exactamente `./build.sh` (con el punto y la barra)

---

### **Start Command** (Requerido)
```
gunicorn korebase.wsgi:application
```

**Explicación**: Este comando inicia el servidor WSGI de producción.

**⚠️ IMPORTANTE**: 
- NO uses `python manage.py runserver` (es solo para desarrollo)
- Usa exactamente `gunicorn korebase.wsgi:application`

---

### **Instance Type** (Requerido)

Tienes 2 opciones:

#### **Opción 1: Free** (Recomendado para pruebas)
- **RAM**: 512 MB
- **CPU**: 0.1 CPU
- **Precio**: $0/mes
- **Limitaciones**:
  - Se apaga después de 15 minutos de inactividad
  - Tarda ~30 segundos en despertar
  - No soporta SSH, trailing, ni persistent disks

**✅ Selecciona esta opción para empezar**

#### **Opción 2: Starter** (Para producción real)
- **RAM**: Más memoria
- **CPU**: Más CPU
- **Precio**: ~$7/mes
- **Ventajas**:
  - Siempre activo
  - Mejor rendimiento
  - Soporta SSH y más features

**Recomendación**: Empieza con **Free** para probar, luego actualiza a **Starter** cuando esté todo funcionando.

---

## 🔐 Variables de Entorno (CRÍTICO)

**⚠️ MUY IMPORTANTE**: Antes de hacer clic en "Create Web Service", debes configurar las variables de entorno.

### **Cómo Agregar Variables**:

1. **Desplázate hacia abajo** en el formulario
2. Busca la sección **"Environment Variables"** o **"Advanced"**
3. Haz clic en **"Add Environment Variable"** (o similar)
4. Agrega las siguientes 7 variables **UNA POR UNA**:

---

### **Variable 1: SECRET_KEY**
```
Key:   SECRET_KEY
Value: evn*+)c*si7jb3!o_)%2!xhgu(mtroz8yv*5q$_7&i3bu(b@i*
```

---

### **Variable 2: DEBUG**
```
Key:   DEBUG
Value: False
```

---

### **Variable 3: PYTHON_VERSION**
```
Key:   PYTHON_VERSION
Value: 3.11.9
```

---

### **Variable 4: DATABASE_URL**
```
Key:   DATABASE_URL
Value: [TU CONNECTION STRING DE NEON.TECH]
```

**Ejemplo**:
```
postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/korebase?sslmode=require
```

**⚠️ IMPORTANTE**: Debe terminar con `?sslmode=require`

---

### **Variable 5: CLOUDINARY_CLOUD_NAME**
```
Key:   CLOUDINARY_CLOUD_NAME
Value: [TU CLOUD NAME DE CLOUDINARY]
```

**Ejemplo**: `dxxxxxxxxx`

---

### **Variable 6: CLOUDINARY_API_KEY**
```
Key:   CLOUDINARY_API_KEY
Value: [TU API KEY DE CLOUDINARY]
```

**Ejemplo**: `123456789012345`

---

### **Variable 7: CLOUDINARY_API_SECRET**
```
Key:   CLOUDINARY_API_SECRET
Value: [TU API SECRET DE CLOUDINARY]
```

**Ejemplo**: `xxxxxxxxxxxxxxxxxxxx`

---

## ✅ Resumen de Configuración

Antes de hacer clic en "Create Web Service", verifica:

| Campo | Valor |
|-------|-------|
| **Name** | `korebase-erp` |
| **Project** | `My project` |
| **Language** | `Python 3` |
| **Branch** | `main` |
| **Region** | `Virginia (US East)` |
| **Root Directory** | (vacío) |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn korebase.wsgi:application` |
| **Instance Type** | `Free` |

**Variables de Entorno** (7 variables):
- [x] SECRET_KEY
- [x] DEBUG
- [x] PYTHON_VERSION
- [x] DATABASE_URL
- [x] CLOUDINARY_CLOUD_NAME
- [x] CLOUDINARY_API_KEY
- [x] CLOUDINARY_API_SECRET

---

## 🚀 Crear el Servicio

1. **Verifica** que todos los campos estén correctos
2. **Verifica** que las 7 variables de entorno estén configuradas
3. Haz clic en **"Create Web Service"** (botón azul al final)
4. **Espera** 3-5 minutos mientras Render despliega

---

## 📊 Qué Esperar Después

### **Durante el Build** (3-5 minutos):

Verás en los logs:

```
==> Cloning from https://github.com/Leonel-Ricebaguila/korebase-erp...
==> Checking out commit 46667c1...
==> Running build command './build.sh'...

🚀 Installing dependencies...
Collecting Django>=5.0
...
Successfully installed Django-5.0.1 psycopg2-binary-2.9.9 ...

📦 Collecting static files...
180 static files copied to '/opt/render/project/src/staticfiles'

🗄️  Running database migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, logistica, produccion, financiero
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...

✅ Build completed successfully!

==> Starting service with 'gunicorn korebase.wsgi:application'...
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 23
```

### **Cuando Esté Listo**:

- Estado cambiará a **"Live"** (verde)
- Verás tu URL: `https://korebase-erp.onrender.com`
- Podrás visitar la aplicación

---

## 🐛 Si Algo Sale Mal

### **Error: "Build failed"**

**Posibles causas**:
1. `build.sh` no tiene permisos de ejecución
2. Alguna variable de entorno falta
3. Error en `requirements.txt`

**Solución**:
- Revisa los logs en Render
- Busca la línea con "ERROR"
- Verifica que todas las variables estén configuradas

### **Error: "Database connection failed"**

**Causa**: `DATABASE_URL` incorrecta

**Solución**:
1. Ve a Neon.tech
2. Copia nuevamente la connection string
3. Verifica que termine con `?sslmode=require`
4. Actualiza la variable en Render

### **Error: "Application failed to start"**

**Causa**: Error en el código o configuración

**Solución**:
- Revisa los logs de runtime (no solo build)
- Busca el error específico
- Verifica que `DEBUG=False` esté configurado

---

## 📞 Siguiente Paso

Una vez que el servicio esté **"Live"**:

1. Copia la URL: `https://korebase-erp.onrender.com`
2. Ábrela en el navegador
3. Deberías ver la página de login
4. Continúa con **FASE 6** del checklist (Crear Superusuario)

---

**¡Éxito con tu deployment!** 🚀

Si tienes dudas sobre algún campo, pregúntame antes de hacer clic en "Create Web Service".
