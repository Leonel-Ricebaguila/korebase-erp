# 🎨 Arquitectura Frontend - KoreBase ERP

## 📋 Tabla de Contenidos

1. [Filosofía de Separación](#filosofía-de-separación)
2. [Estructura de Directorios](#estructura-de-directorios)
3. [Sistema de Plantillas Base](#sistema-de-plantillas-base)
4. [Componentes Reutilizables](#componentes-reutilizables)
5. [Guía de Implementación](#guía-de-implementación)
6. [Convenciones y Mejores Prácticas](#convenciones-y-mejores-prácticas)
7. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## 🎯 Filosofía de Separación

### Principios Fundamentales

1. **Separación de Responsabilidades**: El frontend (presentación) está completamente desacoplado del backend (lógica de negocio)
2. **Modularidad**: Cada componente visual es independiente y reutilizable
3. **Consistencia**: Sistema de diseño unificado a través de variables CSS
4. **Escalabilidad**: Fácil agregar nuevos módulos sin afectar los existentes
5. **Mantenibilidad**: Cambios visuales no requieren tocar la lógica del backend

### Ventajas de esta Arquitectura

✅ **Desarrollo Paralelo**: Frontend y Backend pueden trabajarse simultáneamente  
✅ **Reutilización**: Componentes se usan en múltiples vistas  
✅ **Testing**: Más fácil probar la lógica sin preocuparse por el UI  
✅ **Rediseño**: Cambiar completamente el diseño sin tocar Python  
✅ **Performance**: CSS y JS se cachean eficientemente  

---

## 📁 Estructura de Directorios

```
korebase-django/
├── templates/                      # Plantillas globales
│   ├── layouts/                    # Layouts base
│   │   ├── base.html              # Layout principal
│   │   ├── auth.html              # Layout para autenticación
│   │   └── admin.html             # Layout para admin
│   ├── components/                 # Componentes reutilizables
│   │   ├── navigation/
│   │   │   ├── sidebar.html       # Barra lateral
│   │   │   ├── topbar.html        # Barra superior
│   │   │   └── breadcrumb.html    # Migas de pan
│   │   ├── cards/
│   │   │   ├── metric_card.html   # Tarjeta de métrica
│   │   │   ├── info_card.html     # Tarjeta informativa
│   │   │   └── action_card.html   # Tarjeta de acción
│   │   ├── forms/
│   │   │   ├── input.html         # Input genérico
│   │   │   ├── select.html        # Select genérico
│   │   │   └── button.html        # Botón genérico
│   │   ├── tables/
│   │   │   ├── data_table.html    # Tabla de datos
│   │   │   └── pagination.html    # Paginación
│   │   └── alerts/
│   │       ├── message.html       # Mensaje de sistema
│   │       └── notification.html  # Notificación
│   └── pages/                      # Páginas especiales
│       ├── 404.html
│       ├── 500.html
│       └── maintenance.html
│
├── static/                         # Archivos estáticos
│   ├── css/
│   │   ├── design-system.css      # Variables y sistema de diseño
│   │   ├── layouts.css            # Estilos de layouts
│   │   ├── components.css         # Estilos de componentes
│   │   ├── utilities.css          # Clases utilitarias
│   │   └── modules/               # Estilos por módulo
│   │       ├── core.css
│   │       ├── logistica.css
│   │       ├── produccion.css
│   │       └── financiero.css
│   ├── js/
│   │   ├── app.js                 # JavaScript principal
│   │   ├── components/            # JS de componentes
│   │   │   ├── sidebar.js
│   │   │   ├── modal.js
│   │   │   └── datatable.js
│   │   └── modules/               # JS por módulo
│   │       ├── core.js
│   │       ├── logistica.js
│   │       ├── produccion.js
│   │       └── financiero.js
│   ├── images/
│   │   ├── logos/
│   │   ├── icons/
│   │   └── backgrounds/
│   └── fonts/
│
├── core/templates/core/            # Templates específicos del módulo
│   ├── dashboard.html
│   └── login.html
│
├── logistica/templates/logistica/
│   ├── index.html
│   ├── inventory_list.html
│   └── product_form.html
│
├── produccion/templates/produccion/
│   └── index.html
│
└── financiero/templates/financiero/
    └── index.html
```

---

## 🏗️ Sistema de Plantillas Base

### 1. Layout Principal (`templates/layouts/base.html`)

Este es el layout maestro que contiene la estructura HTML completa.

**Responsabilidades:**
- Estructura HTML5 completa
- Carga de CSS y JavaScript globales
- Meta tags y SEO
- Bloques extensibles para contenido

**Bloques disponibles:**
- `{% block title %}` - Título de la página
- `{% block extra_css %}` - CSS adicional
- `{% block content %}` - Contenido principal
- `{% block extra_js %}` - JavaScript adicional

### 2. Layout de Autenticación (`templates/layouts/auth.html`)

Layout simplificado para páginas de login, registro, recuperación de contraseña.

**Características:**
- Sin sidebar ni navegación
- Diseño centrado
- Fondo personalizado
- Formularios estilizados

### 3. Layout de Administración (`templates/layouts/admin.html`)

Layout para vistas administrativas con permisos especiales.

**Características:**
- Sidebar con opciones de admin
- Indicadores de permisos
- Herramientas de gestión

---

## 🧩 Componentes Reutilizables

### Filosofía de Componentes

Cada componente es un archivo HTML independiente que recibe parámetros mediante `{% include %}` con contexto.

### Ejemplo de Uso

```django
{# En cualquier template #}
{% include 'components/cards/metric_card.html' with 
    label="Usuarios Activos"
    value=total_users
    icon="fa-users"
    trend="positive"
    trend_text="+12% este mes"
%}
```

### Componentes Disponibles

#### 1. **Navegación**

**Sidebar** (`components/navigation/sidebar.html`)
```django
{% include 'components/navigation/sidebar.html' with user=request.user %}
```

**Topbar** (`components/navigation/topbar.html`)
```django
{% include 'components/navigation/topbar.html' with 
    page_title="Dashboard"
    show_search=True
%}
```

**Breadcrumb** (`components/navigation/breadcrumb.html`)
```django
{% include 'components/navigation/breadcrumb.html' with 
    items=breadcrumb_items
%}
```

#### 2. **Tarjetas (Cards)**

**Metric Card** (`components/cards/metric_card.html`)
```django
{% include 'components/cards/metric_card.html' with 
    label="Ventas del Mes"
    value="$45,231"
    icon="fa-dollar-sign"
    trend="positive"
    trend_text="+23%"
    color="success"
%}
```

**Info Card** (`components/cards/info_card.html`)
```django
{% include 'components/cards/info_card.html' with 
    title="Información del Sistema"
    content=system_info
    icon="fa-info-circle"
%}
```

#### 3. **Formularios**

**Input Field** (`components/forms/input.html`)
```django
{% include 'components/forms/input.html' with 
    name="username"
    label="Usuario"
    type="text"
    placeholder="Ingresa tu usuario"
    icon="fa-user"
    required=True
%}
```

**Select Field** (`components/forms/select.html`)
```django
{% include 'components/forms/select.html' with 
    name="category"
    label="Categoría"
    options=categories
    icon="fa-list"
%}
```

**Button** (`components/forms/button.html`)
```django
{% include 'components/forms/button.html' with 
    text="Guardar Cambios"
    type="submit"
    style="primary"
    icon="fa-save"
%}
```

#### 4. **Tablas**

**Data Table** (`components/tables/data_table.html`)
```django
{% include 'components/tables/data_table.html' with 
    headers=table_headers
    rows=table_data
    actions=True
%}
```

#### 5. **Alertas**

**Message Alert** (`components/alerts/message.html`)
```django
{% include 'components/alerts/message.html' with 
    type="success"
    icon="fa-check-circle"
    message="Operación completada exitosamente"
%}
```

---

## 🚀 Guía de Implementación

### Paso 1: Crear el Sistema de Diseño

Crea `static/css/design-system.css` con todas las variables CSS:

```css
:root {
    /* Colores primarios */
    --color-primary: #714B67;
    --color-secondary: #5a3b52;
    
    /* Colores de estado */
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    --color-info: #3b82f6;
    
    /* Escala de grises */
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-600: #4b5563;
    --color-gray-800: #1f2937;
    
    /* Espaciado */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Tipografía */
    --font-family: 'Inter', -apple-system, sans-serif;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    
    /* Bordes */
    --border-radius-sm: 0.375rem;
    --border-radius-md: 0.5rem;
    --border-radius-lg: 0.75rem;
    
    /* Sombras */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Paso 2: Crear Layouts Base

**`templates/layouts/base.html`** - Ver implementación completa en la sección de ejemplos.

### Paso 3: Crear Componentes

Cada componente debe:
1. Aceptar parámetros vía contexto
2. Tener valores por defecto
3. Ser visualmente consistente
4. Ser accesible (ARIA labels)

### Paso 4: Actualizar Vistas Existentes

**Antes:**
```python
def dashboard_view(request):
    context = {'user': request.user}
    return render(request, 'core/dashboard.html', context)
```

**Después (sin cambios en el backend):**
```python
def dashboard_view(request):
    # La lógica permanece igual
    context = {
        'user': request.user,
        'total_users': User.objects.count(),
        'metrics': get_dashboard_metrics(),  # Solo datos
    }
    return render(request, 'core/dashboard.html', context)
```

**Template actualizado:**
```django
{% extends 'layouts/base.html' %}

{% block content %}
    {% for metric in metrics %}
        {% include 'components/cards/metric_card.html' with 
            label=metric.label
            value=metric.value
            icon=metric.icon
        %}
    {% endfor %}
{% endblock %}
```

### Paso 5: Migración Gradual

1. **No toques el backend**: Las vistas siguen igual
2. **Crea nuevos layouts**: `layouts/base.html`, `layouts/auth.html`
3. **Extrae componentes**: Identifica patrones repetidos
4. **Actualiza templates**: Usa `{% extends %}` y `{% include %}`
5. **Prueba**: Verifica que todo funcione igual visualmente

---

## 📐 Convenciones y Mejores Prácticas

### Nomenclatura

**Archivos:**
- Layouts: `snake_case.html` (ej: `base.html`, `admin_layout.html`)
- Componentes: `snake_case.html` (ej: `metric_card.html`)
- CSS: `kebab-case.css` (ej: `design-system.css`)
- JS: `camelCase.js` (ej: `dataTable.js`)

**Clases CSS:**
- Prefijo por módulo: `erp-`, `core-`, `log-`
- BEM para componentes: `.card__header`, `.card__body`
- Utilidades: `.flex`, `.gap-4`, `.text-center`

### Estructura de un Componente

```django
{# components/cards/metric_card.html #}
{# 
    Parámetros:
    - label: str (requerido) - Etiqueta de la métrica
    - value: str|int (requerido) - Valor a mostrar
    - icon: str (opcional) - Clase de Font Awesome
    - trend: str (opcional) - 'positive', 'negative', 'neutral'
    - trend_text: str (opcional) - Texto del trend
    - color: str (opcional) - 'primary', 'success', 'warning', 'danger'
#}

<div class="metric-card {% if color %}metric-card--{{ color }}{% endif %}">
    <div class="metric-card__header">
        <span class="metric-card__label">{{ label }}</span>
        {% if icon %}
        <span class="metric-card__icon">
            <i class="fas {{ icon }}"></i>
        </span>
        {% endif %}
    </div>
    <div class="metric-card__value">{{ value }}</div>
    {% if trend %}
    <div class="metric-card__trend metric-card__trend--{{ trend }}">
        <i class="fas fa-arrow-{{ trend|yesno:'up,down,right' }}"></i>
        {{ trend_text|default:"Sin cambios" }}
    </div>
    {% endif %}
</div>
```

### Patrón de Vista (Backend)

```python
# ✅ CORRECTO: Vista solo maneja lógica
def inventory_list_view(request):
    """Lista de productos en inventario"""
    # 1. Obtener datos
    products = Product.objects.select_related('category').all()
    
    # 2. Procesar lógica de negocio
    low_stock = products.filter(quantity__lt=10).count()
    
    # 3. Preparar contexto (solo datos)
    context = {
        'products': products,
        'low_stock_count': low_stock,
        'categories': Category.objects.all(),
    }
    
    # 4. Renderizar (el template maneja la presentación)
    return render(request, 'logistica/inventory_list.html', context)
```

```django
{# ✅ CORRECTO: Template maneja presentación #}
{% extends 'layouts/base.html' %}

{% block content %}
    {# Alerta si hay stock bajo #}
    {% if low_stock_count > 0 %}
        {% include 'components/alerts/message.html' with 
            type="warning"
            message="Hay "|add:low_stock_count|add:" productos con stock bajo"
        %}
    {% endif %}
    
    {# Tabla de productos #}
    {% include 'components/tables/data_table.html' with 
        headers=table_headers
        rows=products
        actions=True
    %}
{% endblock %}
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Crear una Nueva Vista de Módulo

**Backend (`logistica/views.py`):**
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product, Warehouse

@login_required
def warehouse_dashboard(request):
    """Dashboard del módulo de logística"""
    warehouses = Warehouse.objects.all()
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(quantity__lt=10).count()
    
    context = {
        'warehouses': warehouses,
        'total_products': total_products,
        'low_stock': low_stock,
    }
    return render(request, 'logistica/warehouse_dashboard.html', context)
```

**Frontend (`logistica/templates/logistica/warehouse_dashboard.html`):**
```django
{% extends 'layouts/base.html' %}

{% block title %}Dashboard de Almacenes - KoreBase{% endblock %}
{% block page_title %}Gestión de Almacenes{% endblock %}

{% block content %}
    {# Breadcrumb #}
    {% include 'components/navigation/breadcrumb.html' with items=breadcrumb %}
    
    {# Métricas #}
    <div class="metrics-grid">
        {% include 'components/cards/metric_card.html' with 
            label="Total de Productos"
            value=total_products
            icon="fa-boxes"
            color="primary"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Stock Bajo"
            value=low_stock
            icon="fa-exclamation-triangle"
            color="warning"
        %}
    </div>
    
    {# Lista de almacenes #}
    <div class="card">
        <div class="card__header">
            <h2>Almacenes Activos</h2>
            {% include 'components/forms/button.html' with 
                text="Nuevo Almacén"
                style="primary"
                icon="fa-plus"
            %}
        </div>
        <div class="card__body">
            {% for warehouse in warehouses %}
                {% include 'components/cards/info_card.html' with 
                    title=warehouse.name
                    content=warehouse.location
                    icon="fa-warehouse"
                %}
            {% endfor %}
        </div>
    </div>
{% endblock %}
```

### Ejemplo 2: Formulario Modular

**Backend (`logistica/views.py`):**
```python
@login_required
def product_create(request):
    """Crear nuevo producto"""
    if request.method == 'POST':
        # Lógica de guardado
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('logistica:product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'logistica/product_form.html', context)
```

**Frontend (`logistica/templates/logistica/product_form.html`):**
```django
{% extends 'layouts/base.html' %}

{% block content %}
    <div class="card">
        <div class="card__header">
            <h2>Nuevo Producto</h2>
        </div>
        <div class="card__body">
            <form method="post" class="form">
                {% csrf_token %}
                
                {% include 'components/forms/input.html' with 
                    name="name"
                    label="Nombre del Producto"
                    type="text"
                    icon="fa-box"
                    required=True
                %}
                
                {% include 'components/forms/select.html' with 
                    name="category"
                    label="Categoría"
                    options=categories
                    icon="fa-list"
                %}
                
                {% include 'components/forms/input.html' with 
                    name="quantity"
                    label="Cantidad"
                    type="number"
                    icon="fa-hashtag"
                %}
                
                <div class="form__actions">
                    {% include 'components/forms/button.html' with 
                        text="Guardar"
                        type="submit"
                        style="primary"
                        icon="fa-save"
                    %}
                    
                    {% include 'components/forms/button.html' with 
                        text="Cancelar"
                        type="button"
                        style="secondary"
                        onclick="window.history.back()"
                    %}
                </div>
            </form>
        </div>
    </div>
{% endblock %}
```

---

## 🎨 Personalización por Rol de Usuario

### Vista de Usuario Normal

```django
{% extends 'layouts/base.html' %}

{% block content %}
    {# Solo ve sus propios datos #}
    <div class="user-dashboard">
        {% include 'components/cards/metric_card.html' with 
            label="Mis Tareas"
            value=user_tasks_count
        %}
    </div>
{% endblock %}
```

### Vista de Administrador

```django
{% extends 'layouts/admin.html' %}

{% block content %}
    {# Ve todos los datos del sistema #}
    <div class="admin-dashboard">
        {% include 'components/cards/metric_card.html' with 
            label="Total de Usuarios"
            value=all_users_count
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Tareas Globales"
            value=all_tasks_count
        %}
    </div>
{% endblock %}
```

---

## 🔄 Flujo de Trabajo Recomendado

### Para Agregar una Nueva Vista

1. **Backend (Python):**
   ```python
   # views.py - Solo lógica
   def my_new_view(request):
       data = get_data_from_database()
       return render(request, 'module/my_view.html', {'data': data})
   ```

2. **Frontend (HTML):**
   ```django
   {% extends 'layouts/base.html' %}
   {% block content %}
       {% include 'components/cards/info_card.html' with content=data %}
   {% endblock %}
   ```

3. **Estilos (CSS):**
   ```css
   /* static/css/modules/module.css */
   .my-custom-style {
       /* Estilos específicos */
   }
   ```

### Para Modificar el Diseño

1. **Identifica el componente** a modificar
2. **Edita solo el archivo del componente** (ej: `components/cards/metric_card.html`)
3. **Actualiza el CSS** correspondiente
4. **No toques el backend** - las vistas siguen igual

---

## 📚 Recursos Adicionales

- **Design System**: `static/css/design-system.css`
- **Componentes**: `templates/components/`
- **Ejemplos**: Ver templates existentes en cada módulo
- **Documentación Django Templates**: https://docs.djangoproject.com/en/5.0/topics/templates/

---

## ✅ Checklist de Implementación

- [ ] Crear estructura de directorios
- [ ] Implementar sistema de diseño (CSS variables)
- [ ] Crear layouts base (base.html, auth.html, admin.html)
- [ ] Extraer componentes comunes
- [ ] Migrar templates existentes
- [ ] Documentar componentes nuevos
- [ ] Probar en diferentes navegadores
- [ ] Validar accesibilidad (ARIA)
- [ ] Optimizar performance (minificar CSS/JS)

---

**Última actualización**: 29 de enero de 2026  
**Versión**: 1.0  
**Autor**: Equipo de Desarrollo KoreBase
