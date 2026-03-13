# 📘 KoreBase ERP - Manual Maestro y Guía de Desarrollo

Este documento centraliza toda la información vital del proyecto. El resto de documentación detallada se encuentra en esta misma carpeta `docs/`.

---

## 1. Filosofía y Lógica de Negocio

### ✅ **¿Qué es KoreBase ERP?**
Plataforma de gestión empresarial de inventarios y logística operando **100% en la nube (PaaS)**. 

*   **Accesibilidad:** Acceso vía navegador web, multi-usuario, sin instalación local.
*   **Seguridad:** Registro con validación de identidad (Email corporativo + OTP).
*   **Logística:** Catálogo maestro, stock en tiempo real, movimientos y auditoría.
*   **Dashboard:** Inteligencia de negocio operativa (KPIs de inventario).

### ❌ **¿Qué NO es?**
*   **No es Offline:** Requiere internet constante.
*   **No es Contabilidad Fiscal:** No genera balances ni declaraciones SAT.
*   **No es CRM:** No gestiona ventas comerciales ni marketing.
*   **No es Hardware:** No controla maquinaria industrial directamente.

---

## 2. Mapa de Documentación
Todos los archivos de especificaciones detalladas han sido movidos a la carpeta `docs/` para mantener la raíz limpia.

| Archivo | Descripción |
| :--- | :--- |
| **`KOREPILOT_SPECS.md`** | **[IMPORTANTE]** Especificaciones técnicas, stack y reglas de desarrollo del agente. |
| `GUIA_MODULAR_COMPLETA.md` | Detalle exhaustivo de cada módulo (Core, Logística, etc.). |
| `DEPLOYMENT_GUIDE.md` | Guía paso a paso para desplegar en Render. |
| `RENDER_CONFIG.md` | Configuraciones específicas de variables de entorno en Render. |
| `SECURITY_AUDIT.md` | Reporte y medidas de seguridad implementadas. |

---

## 3. Comandos Frecuentes (Cheatsheet)

### 🛠️ **Desarrollo Local**
```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Correr servidor
python manage.py runserver

# Crear migraciones (al modificar models.py)
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 👤 **Gestión de Usuarios**
```bash
# Crear superusuario (Script automático)
python scripts/create_superuser.py

# Cambiar contraseña manualmente
python scripts/set_password.py
```

### 🚀 **Deploy a Producción**
Todo push a la rama `main` dispara un deploy automático en Render.
```bash
git add .
git commit -m "feat: descripción del cambio"
git push origin main
```

---

## 4. Estructura del Proyecto (Limpia)
*   **`/core`**: Autenticación, Usuarios, Home.
*   **`/logistica`**: Inventarios, Productos, Movimientos.
*   **`/korebase`**: Configuración global (`settings.py`, `urls.py`).
*   **`/docs`**: Documentación del proyecto.
*   **`/scripts`**: Scripts de utilidad Python.
*   **`/static`**: Archivos CSS, JS e Imágenes.
*   **`/templates`**: Plantillas HTML base.
