# 🏢 KoreBase ERP - Sistema de Gestión Empresarial

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Sistema ERP modular desarrollado con Django, diseñado para gestión empresarial integral con arquitectura de monolito modular.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Despliegue](#-despliegue)
- [Seguridad](#-seguridad)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

### **Módulos del ERP**

- 🔐 **Core**: Autenticación, usuarios, permisos y roles
- 📦 **Logística**: Gestión de inventario, almacenes, proveedores
- 🏭 **Producción**: Órdenes de trabajo, planificación, recursos
- 💰 **Financiero**: Contabilidad, facturación, presupuestos

### **Tecnologías**

- **Backend**: Django 5.0+, Python 3.11+
- **Base de Datos**: PostgreSQL (Neon.tech) / SQLite (desarrollo)
- **Archivos Multimedia**: Cloudinary
- **Archivos Estáticos**: WhiteNoise
- **Despliegue**: Render.com
- **Frontend**: Templates modulares, componentes reutilizables

### **Características Técnicas**

- ✅ Arquitectura modular (Monolito Modular)
- ✅ Separación frontend/backend
- ✅ Componentes reutilizables
- ✅ Sistema de diseño centralizado
- ✅ Responsive design
- ✅ Optimizado para producción
- ✅ Documentación completa

---

## 🏗️ Arquitectura

```
korebase-django/
├── core/                    # Módulo de autenticación
├── logistica/               # Módulo de logística (SCM)
├── produccion/              # Módulo de producción (MRP)
├── financiero/              # Módulo financiero
├── korebase/                # Configuración del proyecto
├── templates/               # Templates globales
│   ├── layouts/            # Layouts base
│   └── components/         # Componentes reutilizables
├── static/                  # Archivos estáticos (CSS, JS)
├── requirements.txt         # Dependencias
├── build.sh                 # Script de build (Render.com)
└── manage.py                # CLI de Django
```

**Arquitectura de Monolito Modular**: Cada módulo es independiente pero comparte la misma base de datos y configuración.

---

## 🚀 Instalación

### **Requisitos Previos**

- Python 3.11 o superior
- Git
- PostgreSQL (opcional, para desarrollo local)

### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/TU_USUARIO/korebase-django.git
cd korebase-django
```

### **Paso 2: Crear Entorno Virtual**

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Paso 3: Instalar Dependencias**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Paso 4: Configurar Variables de Entorno**

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
```

**Generar SECRET_KEY segura:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Paso 5: Aplicar Migraciones**

```bash
python manage.py migrate
```

### **Paso 6: Crear Superusuario**

```bash
python manage.py createsuperuser
```

### **Paso 7: Ejecutar Servidor de Desarrollo**

```bash
python manage.py runserver
```

Visita: `http://localhost:8000`

---

## ⚙️ Configuración

### **Variables de Entorno**

Crea un archivo `.env` basado en `.env.example`:

```env
# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=False

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/korebase

# Cloudinary (Archivos multimedia)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### **Configuración de Base de Datos**

**Desarrollo (SQLite):**
```python
# No configurar DATABASE_URL
# Django usará SQLite automáticamente
```

**Producción (PostgreSQL):**
```python
# Configurar DATABASE_URL en .env
DATABASE_URL=postgresql://user:password@host:5432/korebase
```

---

## 🌐 Despliegue

### **Render.com + Neon.tech + Cloudinary**

1. **Crea una cuenta en**:
   - [Render.com](https://render.com) - Hosting
   - [Neon.tech](https://neon.tech) - PostgreSQL
   - [Cloudinary](https://cloudinary.com) - Archivos multimedia

2. **Configura variables de entorno** en Render.com

3. **Despliega**:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn korebase.wsgi:application`

**Guía completa**: Ver [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)

---

## 🔒 Seguridad

### ⚠️ **IMPORTANTE**

Este repositorio **NO contiene credenciales reales**. Todas las configuraciones sensibles se manejan mediante variables de entorno.

### **Antes de Desplegar a Producción:**

1. ✅ **Genera una SECRET_KEY segura**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. ✅ **Configura `DEBUG=False`** en producción

3. ✅ **Cambia la contraseña de admin**
   - NO uses `admin123` (es solo para desarrollo)
   - Crea un superusuario con contraseña segura

4. ✅ **Configura HTTPS** (Render.com lo hace automáticamente)

5. ✅ **Configura ALLOWED_HOSTS** correctamente

6. ✅ **Usa variables de entorno** para todas las credenciales

### **Archivos Protegidos**

Los siguientes archivos están en `.gitignore` y **NO se suben al repositorio**:

- `.env` - Variables de entorno
- `db.sqlite3` - Base de datos local
- `venv/` - Entorno virtual
- `staticfiles/` - Archivos estáticos compilados

**Auditoría de seguridad**: Ver [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md)

---

## 📚 Documentación

### **Guías Disponibles**

- 📖 **[FRONTEND_ARCHITECTURE.md](FRONTEND_ARCHITECTURE.md)** - Arquitectura frontend modular
- 🚀 **[QUICK_START_FRONTEND.md](QUICK_START_FRONTEND.md)** - Guía rápida de frontend
- 📋 **[GUIA_MODULAR_COMPLETA.md](GUIA_MODULAR_COMPLETA.md)** - Guía completa de desarrollo modular
- 🌐 **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Guía de despliegue
- 🪟 **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Configuración en Windows 11
- 🔒 **[SECURITY_AUDIT.md](SECURITY_AUDIT.md)** - Auditoría de seguridad

### **Estructura de Módulos**

Cada módulo sigue la misma estructura:

```
[modulo]/
├── models.py           # Modelos de datos
├── views.py            # Lógica de negocio
├── urls.py             # Rutas
├── admin.py            # Configuración de admin
├── forms.py            # Formularios
├── templates/          # Templates del módulo
└── tests.py            # Tests
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### **Convenciones de Commits**

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Cambios en documentación
- `style:` Cambios de formato
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👥 Autores

- **Equipo KoreBase** - *Desarrollo inicial*

---

## 🙏 Agradecimientos

- Universidad Politécnica de Yucatán
- Comunidad de Django
- Contribuidores del proyecto

---

## 📞 Soporte

¿Tienes preguntas? Abre un [issue](https://github.com/TU_USUARIO/korebase-django/issues) o consulta la [documentación](FRONTEND_ARCHITECTURE.md).

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**
