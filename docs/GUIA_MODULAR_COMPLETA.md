# 📋 GUÍA COMPLETA: Separación Frontend/Backend - KoreBase ERP

## 🎯 Objetivo Logrado

Has solicitado separar el **frontend (layout/presentación)** del **backend (lógica)** para poder mejorar el apartado visual sin afectar la funcionalidad. 

**✅ COMPLETADO**: Sistema modular implementado que permite modificar completamente el diseño sin tocar Python.

---

## 📁 Archivos Creados

### 📚 Documentación

1. **`FRONTEND_ARCHITECTURE.md`** - Arquitectura completa del sistema frontend
2. **`QUICK_START_FRONTEND.md`** - Guía rápida de implementación
3. **`WINDOWS_SETUP.md`** - Guía de configuración en Windows 11
4. **`static/README.md`** - Documentación del directorio static

### 🎨 Sistema de Diseño

5. **`static/css/design-system.css`** - Variables CSS y sistema de diseño
6. **`static/js/app.js`** - JavaScript global con utilidades

### 🏗️ Layouts Base

7. **`templates/layouts/base.html`** - Layout principal modular

### 🧩 Componentes Reutilizables

8. **`templates/components/navigation/sidebar.html`** - Barra lateral
9. **`templates/components/navigation/topbar.html`** - Barra superior
10. **`templates/components/cards/metric_card.html`** - Tarjeta de métrica
11. **`templates/components/alerts/message.html`** - Alertas/mensajes

---

## 🎨 PAUTAS PARA TRABAJAR DE FORMA MODULAR

### 1️⃣ Para Vistas de Usuario Normal

**Ubicación**: `[modulo]/templates/[modulo]/[vista].html`

**Ejemplo**: Vista de inventario para usuario

```django
{# logistica/templates/logistica/my_inventory.html #}
{% extends 'layouts/base.html' %}

{% block title %}Mi Inventario - KoreBase{% endblock %}
{% block page_title %}Mi Inventario{% endblock %}

{% block content %}
    {# El usuario solo ve sus propios datos #}
    <div class="grid grid-cols-2 gap-4">
        {% include 'components/cards/metric_card.html' with 
            label="Mis Productos Asignados"
            value=my_products_count
            icon="fa-box"
            color="primary"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Tareas Pendientes"
            value=my_pending_tasks
            icon="fa-tasks"
            color="warning"
        %}
    </div>
    
    {# Lista de productos del usuario #}
    <div class="bg-white rounded-lg shadow-md p-6 mt-4">
        <h2 class="text-xl font-bold mb-4">Mis Productos</h2>
        {% for product in my_products %}
            <div class="border-b py-3">
                <h3 class="font-semibold">{{ product.name }}</h3>
                <p class="text-sm text-gray-600">Cantidad: {{ product.quantity }}</p>
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

**Backend (NO CAMBIAR)**:
```python
@login_required
def my_inventory_view(request):
    # Filtrar solo productos del usuario actual
    my_products = Product.objects.filter(assigned_to=request.user)
    
    context = {
        'my_products': my_products,
        'my_products_count': my_products.count(),
        'my_pending_tasks': Task.objects.filter(user=request.user, status='pending').count(),
    }
    return render(request, 'logistica/my_inventory.html', context)
```

---

### 2️⃣ Para Vistas de Administrador

**Ubicación**: `[modulo]/templates/[modulo]/admin_[vista].html`

**Ejemplo**: Vista de inventario para administrador

```django
{# logistica/templates/logistica/admin_inventory.html #}
{% extends 'layouts/base.html' %}

{% block title %}Administración de Inventario - KoreBase{% endblock %}
{% block page_title %}Panel de Administración - Inventario{% endblock %}

{% block content %}
    {# Indicador de permisos de admin #}
    <div class="bg-primary-50 border-l-4 border-primary p-4 mb-6">
        <div class="flex items-center">
            <i class="fas fa-shield-alt text-primary mr-3"></i>
            <span class="font-semibold text-primary">Vista de Administrador</span>
        </div>
    </div>
    
    {# Métricas globales #}
    <div class="grid grid-cols-4 gap-4 mb-6">
        {% include 'components/cards/metric_card.html' with 
            label="Total de Productos"
            value=total_products
            icon="fa-boxes"
            color="primary"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Usuarios Activos"
            value=active_users
            icon="fa-users"
            color="info"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Stock Crítico"
            value=critical_stock
            icon="fa-exclamation-triangle"
            color="danger"
        %}
        
        {% include 'components/cards/metric_card.html' with 
            label="Valor Total"
            value=total_value
            icon="fa-dollar-sign"
            color="success"
        %}
    </div>
    
    {# Tabla completa de productos #}
    <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">Todos los Productos</h2>
            <button class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary-dark">
                <i class="fas fa-plus mr-2"></i>Nuevo Producto
            </button>
        </div>
        
        <table class="w-full">
            <thead>
                <tr class="border-b">
                    <th class="text-left py-3">Producto</th>
                    <th class="text-left py-3">Categoría</th>
                    <th class="text-left py-3">Cantidad</th>
                    <th class="text-left py-3">Asignado a</th>
                    <th class="text-left py-3">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for product in all_products %}
                <tr class="border-b hover:bg-gray-50">
                    <td class="py-3">{{ product.name }}</td>
                    <td class="py-3">{{ product.category }}</td>
                    <td class="py-3">{{ product.quantity }}</td>
                    <td class="py-3">{{ product.assigned_to.username|default:"Sin asignar" }}</td>
                    <td class="py-3">
                        <button class="text-primary hover:text-primary-dark">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="text-danger hover:text-danger-dark ml-3">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}
```

**Backend (con verificación de permisos)**:
```python
@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo administradores
def admin_inventory_view(request):
    # Ver TODOS los productos
    all_products = Product.objects.select_related('assigned_to', 'category').all()
    
    context = {
        'all_products': all_products,
        'total_products': all_products.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'critical_stock': all_products.filter(quantity__lt=10).count(),
        'total_value': sum(p.price * p.quantity for p in all_products),
    }
    return render(request, 'logistica/admin_inventory.html', context)
```

---

### 3️⃣ Para Cada Módulo del ERP

#### 📦 Módulo: LOGÍSTICA

**Vistas de Usuario:**
- `logistica/my_inventory.html` - Mi inventario asignado
- `logistica/my_tasks.html` - Mis tareas de logística
- `logistica/request_product.html` - Solicitar producto

**Vistas de Administrador:**
- `logistica/admin_inventory.html` - Gestión completa de inventario
- `logistica/admin_warehouses.html` - Gestión de almacenes
- `logistica/admin_suppliers.html` - Gestión de proveedores
- `logistica/admin_reports.html` - Reportes y estadísticas

#### 🏭 Módulo: PRODUCCIÓN

**Vistas de Usuario:**
- `produccion/my_orders.html` - Mis órdenes de trabajo
- `produccion/my_schedule.html` - Mi horario de producción
- `produccion/report_progress.html` - Reportar avance

**Vistas de Administrador:**
- `produccion/admin_orders.html` - Todas las órdenes de trabajo
- `produccion/admin_planning.html` - Planificación de producción
- `produccion/admin_resources.html` - Gestión de recursos
- `produccion/admin_efficiency.html` - Métricas de eficiencia

#### 💰 Módulo: FINANCIERO

**Vistas de Usuario:**
- `financiero/my_expenses.html` - Mis gastos
- `financiero/my_invoices.html` - Mis facturas
- `financiero/request_payment.html` - Solicitar pago

**Vistas de Administrador:**
- `financiero/admin_dashboard.html` - Dashboard financiero completo
- `financiero/admin_accounts.html` - Gestión de cuentas
- `financiero/admin_budgets.html` - Gestión de presupuestos
- `financiero/admin_reports.html` - Reportes financieros

---

## 🎨 PATRÓN DE DISEÑO RECOMENDADO

### Para TODAS las vistas (Usuario y Admin)

```django
{% extends 'layouts/base.html' %}

{% block title %}[Título] - KoreBase{% endblock %}
{% block page_title %}[Título de la Página]{% endblock %}

{% block content %}
    {# 1. BREADCRUMB (Opcional) #}
    <nav class="mb-4">
        <a href="/" class="text-gray-600 hover:text-primary">Inicio</a>
        <span class="mx-2">/</span>
        <span class="text-gray-900">[Página Actual]</span>
    </nav>
    
    {# 2. ALERTAS/MENSAJES (Si hay) #}
    {% if show_alert %}
        {% include 'components/alerts/message.html' with 
            type="warning"
            message="Mensaje importante aquí"
        %}
    {% endif %}
    
    {# 3. MÉTRICAS (Dashboard style) #}
    <div class="grid grid-cols-4 gap-4 mb-6">
        {% include 'components/cards/metric_card.html' with 
            label="Métrica 1"
            value=metric1
            icon="fa-icon"
            color="primary"
        %}
        {# Más métricas... #}
    </div>
    
    {# 4. CONTENIDO PRINCIPAL #}
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold mb-4">[Título de Sección]</h2>
        
        {# Tu contenido aquí #}
    </div>
    
    {# 5. ACCIONES RÁPIDAS (Opcional) #}
    <div class="mt-6 flex gap-4">
        <button class="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary-dark">
            <i class="fas fa-plus mr-2"></i>Nueva Acción
        </button>
    </div>
{% endblock %}

{# CSS adicional si es necesario #}
{% block extra_css %}
<style>
    .custom-class {
        /* Estilos personalizados */
    }
</style>
{% endblock %}

{# JavaScript adicional si es necesario #}
{% block extra_js %}
<script>
    // JavaScript personalizado
</script>
{% endblock %}
```

---

## 🔄 FLUJO DE TRABAJO PARA NUEVAS VISTAS

### Paso 1: Crear la Vista en Python (Backend)

```python
# [modulo]/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def my_new_view(request):
    # 1. Obtener datos
    data = Model.objects.filter(user=request.user)
    
    # 2. Procesar lógica
    count = data.count()
    
    # 3. Preparar contexto (SOLO DATOS)
    context = {
        'data': data,
        'count': count,
    }
    
    # 4. Renderizar
    return render(request, '[modulo]/my_new_view.html', context)
```

### Paso 2: Crear el Template (Frontend)

```django
{# [modulo]/templates/[modulo]/my_new_view.html #}
{% extends 'layouts/base.html' %}

{% block content %}
    {# Usar componentes para presentar los datos #}
    {% include 'components/cards/metric_card.html' with 
        value=count
    %}
{% endblock %}
```

### Paso 3: Agregar la URL

```python
# [modulo]/urls.py
from django.urls import path
from . import views

app_name = '[modulo]'

urlpatterns = [
    path('my-view/', views.my_new_view, name='my_new_view'),
]
```

---

## 🎨 PERSONALIZACIÓN VISUAL

### Cambiar Colores Globales

Edita `static/css/design-system.css`:

```css
:root {
    --color-primary: #TU_COLOR;
    --color-success: #TU_COLOR;
    /* etc... */
}
```

### Crear Estilos por Módulo

Crea `static/css/modules/[modulo].css`:

```css
/* Estilos específicos del módulo */
.logistica-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
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

## ✅ CHECKLIST POR VISTA

Cuando crees una nueva vista, verifica:

- [ ] **Backend**: Vista retorna solo datos, sin HTML
- [ ] **Template**: Extiende `layouts/base.html`
- [ ] **Título**: Define `{% block title %}` y `{% block page_title %}`
- [ ] **Componentes**: Usa componentes reutilizables
- [ ] **Responsive**: Usa clases utilitarias (grid, flex, etc.)
- [ ] **Permisos**: Verifica `@login_required` y permisos de admin si aplica
- [ ] **Mensajes**: Maneja mensajes de Django con componente de alerta
- [ ] **Consistencia**: Sigue el patrón de diseño establecido

---

## 📚 RECURSOS DISPONIBLES

1. **`FRONTEND_ARCHITECTURE.md`** - Documentación completa
2. **`QUICK_START_FRONTEND.md`** - Guía rápida
3. **`static/css/design-system.css`** - Variables CSS
4. **`templates/components/`** - Componentes reutilizables
5. **`templates/layouts/base.html`** - Layout base

---

## 🚀 PRÓXIMOS PASOS

1. **Prueba el sistema actual**:
   ```bash
   python manage.py runserver
   ```

2. **Crea tu primera vista modular** siguiendo los ejemplos de arriba

3. **Personaliza el diseño** editando `design-system.css`

4. **Crea componentes adicionales** según los necesites

---

## 💡 VENTAJAS DE ESTE SISTEMA

✅ **Separación total**: Frontend y Backend completamente independientes  
✅ **Reutilización**: Componentes se usan en múltiples vistas  
✅ **Mantenimiento**: Cambios en un componente afectan todas las vistas  
✅ **Escalabilidad**: Fácil agregar nuevos módulos y vistas  
✅ **Consistencia**: Sistema de diseño unificado  
✅ **Flexibilidad**: Personaliza cada vista sin afectar otras  

---

**¡Sistema completamente implementado y listo para usar!** 🎉

Para cualquier duda, consulta la documentación completa en `FRONTEND_ARCHITECTURE.md`.
