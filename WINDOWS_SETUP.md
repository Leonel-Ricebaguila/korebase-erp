# Guía de Configuración para Windows 11

## 📋 Requisitos Previos

- Windows 11
- Python 3.11.9 o superior
- Git instalado
- PowerShell 5.1 o superior

---

## 🚀 Configuración Inicial

### 1. Clonar el Repositorio

```powershell
cd C:\Users\[TU_USUARIO]\Documents
git clone https://github.com/Shermanico/korebase-django.git
cd korebase-django
```

### 2. Configurar Políticas de Ejecución

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### 3. Crear y Activar Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (PowerShell)
.\venv\Scripts\Activate

# Actualizar pip
python -m pip install --upgrade pip setuptools wheel
```

### 4. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

**Nota:** Todas las dependencias son compatibles con Windows. `gunicorn` solo se usa en producción Linux.

---

## ⚙️ Configuración del Proyecto

### 5. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env`:

```powershell
copy .env.example .env
```

Edita el archivo `.env` con tu configuración:

```env
# Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

# Database (SQLite para desarrollo local)
# DATABASE_URL se configura automáticamente para SQLite

# Cloudinary (opcional para desarrollo)
# CLOUDINARY_CLOUD_NAME=your-cloud-name
# CLOUDINARY_API_KEY=your-api-key
# CLOUDINARY_API_SECRET=your-api-secret
```

### 6. Aplicar Migraciones

```powershell
python manage.py migrate
```

### 7. Crear Superusuario

```powershell
python manage.py createsuperuser --username admin --email admin@korebase.local
```

O usar el script incluido:

```powershell
python set_password.py
```

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

---

## 🏃 Ejecutar el Servidor

```powershell
python manage.py runserver
```

Accede a:
- **Aplicación:** http://localhost:8000
- **Admin:** http://localhost:8000/admin

---

## 📁 Estructura del Proyecto (Monolito Modular)

```
korebase-django/
├── core/           # Módulo principal (autenticación, usuarios)
├── financiero/     # Módulo de gestión financiera
├── logistica/      # Módulo de gestión logística
├── produccion/     # Módulo de gestión de producción
├── korebase/       # Configuración del proyecto Django
├── templates/      # Plantillas HTML
├── static/         # Archivos estáticos (CSS, JS, imágenes)
├── manage.py       # Script de gestión de Django
└── requirements.txt # Dependencias del proyecto
```

---

## 🌿 Flujo de Trabajo Git (Gitflow)

### Ramas Principales

- **`main`**: Código en producción
- **`develop`**: Rama de integración para desarrollo

### Ramas de Funcionalidad

```powershell
# Crear nueva funcionalidad
git checkout develop
git checkout -b feature/nombre-funcionalidad

# Trabajar en la funcionalidad
git add .
git commit -m "feat: descripción de la funcionalidad"

# Fusionar a develop
git checkout develop
git merge feature/nombre-funcionalidad
```

### Formato de Commits Semánticos

- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Cambios en documentación
- `style:` Cambios de formato (sin afectar lógica)
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

**Ejemplos:**
```powershell
git commit -m "feat: agregar módulo de inventario"
git commit -m "fix: corregir validación de formulario de login"
git commit -m "docs: actualizar README con instrucciones de Windows"
```

---

## 🔧 Comandos Útiles

### Gestión de Dependencias

```powershell
# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Actualizar dependencias
pip install --upgrade -r requirements.txt
```

### Gestión de Base de Datos

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Resetear base de datos (CUIDADO: borra todos los datos)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Gestión de Archivos Estáticos

```powershell
# Recolectar archivos estáticos
python manage.py collectstatic
```

### Testing

```powershell
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de un módulo específico
python manage.py test core
python manage.py test financiero
```

---

## ⚠️ Problemas Comunes en Windows

### Error: "cannot be loaded because running scripts is disabled"

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error al instalar `psycopg2`

**Solución:** El proyecto ya usa `psycopg2-binary` que es compatible con Windows.

### Error con `gunicorn`

**Solución:** `gunicorn` no funciona en Windows. Para desarrollo usa:
```powershell
python manage.py runserver
```

Para producción en Windows, considera usar `waitress`:
```powershell
pip install waitress
waitress-serve --port=8000 korebase.wsgi:application
```

### Directorio `static` no existe

**Solución:**
```powershell
New-Item -ItemType Directory -Path "static" -Force
```

---

## 📚 Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🆘 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo o abre un issue en el repositorio.
