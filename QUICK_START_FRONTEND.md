# 🚀 Guía Rápida de Implementación - Frontend Modular

## ✅ Checklist de Implementación

### Fase 1: Configuración Inicial (Completada ✓)

- [x] Crear estructura de directorios
- [x] Implementar sistema de diseño (`design-system.css`)
- [x] Crear layout base modular (`layouts/base.html`)
- [x] Crear componentes de navegación (sidebar, topbar)
- [x] Crear componentes básicos (metric_card, message)
- [x] Crear JavaScript global (`app.js`)

### Fase 2: Migración de Templates (Siguiente)

- [ ] Actualizar `core/dashboard.html` para usar nuevos componentes
- [ ] Actualizar `core/login.html` para usar nuevo layout
- [ ] Migrar templates de logística
- [ ] Migrar templates de producción
- [ ] Migrar templates de financiero

### Fase 3: Componentes Adicionales (Opcional)

- [ ] Crear componente de formulario (`components/forms/input.html`)
- [ ] Crear componente de tabla (`components/tables/data_table.html`)
- [ ] Crear componente de breadcrumb (`components/navigation/breadcrumb.html`)
- [ ] Crear componente de botón (`components/forms/button.html`)

---

## 🎯 Cómo Usar el Nuevo Sistema

### 1. Crear una Nueva Vista

**Backend (NO CAMBIAR - Solo datos):**
```python
# logistica/views.py
@login_required
def inventory_dashboard(request):
    products = Product.objects.all()
    low_stock = products.filter(quantity__lt=10).count()
    
    context = {
        'products': products,
        'low_stock_count': low_stock,
        'total_products': products.count(),
    }
    return render(request, 'logistica/inventory_dashboard.html', context)
```

**Frontend (Nuevo template):**
```django
{# logistica/templates/logistica/inventory_dashboard.html #}
{% extends 'layouts/base.html' %}

{% block title %}Inventario - KoreBase{% endblock %}
{% block page_title %}Dashboard de Inventario{% endblock %}

{% block content %}
    {# Métricas #}
    <div class="grid grid-cols-3 gap-4">
        {% include 'components/cards/metric_card.html' with 
            label="Total de Productos"
            value=total_products
            icon="fa-boxes"
            color="primary"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Stock Bajo"
            value=low_stock_count
            icon="fa-exclamation-triangle"
            color="warning"
        %}
    </div>
    
    {# Contenido adicional #}
    <div class="mt-4">
        {# Tu contenido aquí #}
    </div>
{% endblock %}
```

### 2. Usar Componentes

**Tarjeta de Métrica:**
```django
{% include 'components/cards/metric_card.html' with 
    label="Ventas del Mes"
    value="$45,231"
    icon="fa-dollar-sign"
    trend="positive"
    trend_text="+23% vs mes anterior"
    color="success"
%}
```

**Alerta/Mensaje:**
```django
{% include 'components/alerts/message.html' with 
    type="success"
    message="Producto guardado exitosamente"
    dismissible=True
%}
```

### 3. Personalizar Estilos

**Opción A: Usar clases utilitarias (Recomendado)**
```django
<div class="flex items-center gap-4 p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold text-gray-900">Mi Título</h2>
</div>
```

**Opción B: CSS personalizado por módulo**
```css
/* static/css/modules/logistica.css */
.inventory-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-4);
}
```

Luego en tu template:
```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/modules/logistica.css' %}">
{% endblock %}
```

---

## 📝 Ejemplo Completo: Migrar Dashboard Actual

### Paso 1: Actualizar el Template

**Archivo:** `core/templates/core/dashboard.html`

**Antes (actual):**
```django
{% extends 'base.html' %}
{% block content %}
    <div class="erp-card">
        <h2>Bienvenido</h2>
    </div>
{% endblock %}
```

**Después (nuevo):**
```django
{% extends 'layouts/base.html' %}

{% block title %}Dashboard - KoreBase{% endblock %}
{% block page_title %}Dashboard{% endblock %}

{% block content %}
    {# Grid de métricas #}
    <div class="grid grid-cols-4 gap-4 mb-6">
        {% include 'components/cards/metric_card.html' with 
            label="Usuarios"
            value=total_users
            icon="fa-users"
            color="primary"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Inventario"
            value="0"
            icon="fa-boxes"
            color="info"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Órdenes"
            value="0"
            icon="fa-industry"
            color="warning"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Facturas"
            value="0"
            icon="fa-file-invoice-dollar"
            color="success"
        %}
    </div>
    
    {# Contenido adicional #}
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">
            Bienvenido al Sistema ERP KoreBase
        </h2>
        <p class="text-gray-600">
            Panel de control general para la gestión empresarial.
        </p>
    </div>
{% endblock %}
```

### Paso 2: NO Cambiar el Backend

El archivo `core/views.py` permanece IGUAL:
```python
@login_required
def dashboard_view(request):
    context = {
        'user': request.user,
        'total_users': 0,  # TODO: Get actual stats
    }
    return render(request, 'core/dashboard.html', context)
```

---

## 🎨 Personalización Visual

### Cambiar Colores del Sistema

Edita `static/css/design-system.css`:

```css
:root {
    /* Cambiar color primario */
    --color-primary: #714B67;  /* Cambia este valor */
    
    /* Cambiar colores de estado */
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
}
```

### Cambiar Fuente

En `static/css/design-system.css`:

```css
:root {
    --font-family-base: 'Poppins', sans-serif;  /* Cambia aquí */
}
```

Y en `layouts/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## 🔧 Solución de Problemas

### Los estilos no se cargan

1. Verifica que `static/css/design-system.css` existe
2. Ejecuta: `python manage.py collectstatic`
3. Reinicia el servidor: `python manage.py runserver`

### El sidebar no aparece

1. Verifica que estás usando `{% extends 'layouts/base.html' %}`
2. Verifica que el usuario está autenticado
3. Revisa la consola del navegador para errores de JavaScript

### Los componentes no se encuentran

1. Verifica la ruta: `templates/components/[tipo]/[nombre].html`
2. Verifica que usas `{% include 'components/...' %}`
3. Asegúrate de que `APP_DIRS = True` en `settings.py`

---

## 📚 Recursos

- **Documentación completa**: `FRONTEND_ARCHITECTURE.md`
- **Sistema de diseño**: `static/css/design-system.css`
- **Componentes**: `templates/components/`
- **Ejemplos**: Ver templates existentes en cada módulo

---

## 🎯 Próximos Pasos

1. **Prueba el sistema actual**:
   ```bash
   python manage.py runserver
   ```
   Visita: http://localhost:8000

2. **Migra un template**:
   - Empieza con `core/dashboard.html`
   - Usa el ejemplo de arriba
   - Prueba que funcione

3. **Crea nuevos componentes**:
   - Identifica patrones repetidos
   - Crea componente en `templates/components/`
   - Documenta su uso

4. **Personaliza el diseño**:
   - Ajusta colores en `design-system.css`
   - Modifica componentes según necesites
   - Mantén la consistencia

---

## ✅ Ventajas de este Sistema

✅ **Backend intacto**: No tocas Python, solo HTML/CSS  
✅ **Componentes reutilizables**: Escribe una vez, usa en todas partes  
✅ **Fácil mantenimiento**: Cambios en un lugar afectan todo el sistema  
✅ **Diseño consistente**: Variables CSS mantienen uniformidad  
✅ **Responsive**: Funciona en móvil, tablet y desktop  
✅ **Escalable**: Fácil agregar nuevos módulos  

---

**¡Listo para empezar!** 🚀

Si tienes dudas, revisa `FRONTEND_ARCHITECTURE.md` para documentación detallada.
