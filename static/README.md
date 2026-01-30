# 📁 Directorio Static - KoreBase ERP

Este directorio contiene todos los archivos estáticos del proyecto (CSS, JavaScript, imágenes, fuentes).

## 📂 Estructura

```
static/
├── css/
│   ├── design-system.css      # ✅ Sistema de diseño con variables CSS
│   ├── layouts.css            # Estilos de layouts
│   ├── components.css         # Estilos de componentes
│   ├── utilities.css          # Clases utilitarias
│   └── modules/               # Estilos específicos por módulo
│       ├── core.css
│       ├── logistica.css
│       ├── produccion.css
│       └── financiero.css
│
├── js/
│   ├── app.js                 # ✅ JavaScript principal
│   ├── components/            # JS de componentes
│   │   ├── sidebar.js
│   │   ├── modal.js
│   │   └── datatable.js
│   └── modules/               # JS por módulo
│       ├── core.js
│       ├── logistica.js
│       ├── produccion.js
│       └── financiero.js
│
├── images/
│   ├── logos/                 # Logos de la empresa
│   ├── icons/                 # Iconos personalizados
│   └── backgrounds/           # Imágenes de fondo
│
└── fonts/                     # Fuentes personalizadas
```

## ✅ Archivos Creados

Los siguientes archivos ya están creados y listos para usar:

1. **`css/design-system.css`** - Sistema de diseño completo con variables CSS
2. **`js/app.js`** - JavaScript principal con utilidades globales

## 📝 Nota Importante

El directorio `static/` está en `.gitignore` porque los archivos estáticos se recolectan con:

```bash
python manage.py collectstatic
```

Los archivos CSS y JS ya están creados en tu sistema local. Para usarlos:

1. Asegúrate de que existen en `static/css/` y `static/js/`
2. Ejecuta `python manage.py collectstatic` antes de desplegar
3. En desarrollo, Django los sirve automáticamente

## 🚀 Uso

Los archivos estáticos se cargan en los templates con:

```django
{% load static %}

{# CSS #}
<link rel="stylesheet" href="{% static 'css/design-system.css' %}">

{# JavaScript #}
<script src="{% static 'js/app.js' %}"></script>

{# Imágenes #}
<img src="{% static 'images/logos/logo.png' %}" alt="Logo">
```

## 📦 Deployment

En producción, WhiteNoise se encarga de servir los archivos estáticos:

```bash
python manage.py collectstatic --noinput
```

Esto copia todos los archivos de `static/` a `staticfiles/` para producción.
