/**
 * KoreBase ERP - Main JavaScript
 * Funcionalidades globales de la aplicación
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('KoreBase ERP - Sistema inicializado');
    
    // Inicializar componentes
    initSidebar();
    initAlerts();
    initTooltips();
});

/**
 * Inicializar sidebar y navegación móvil
 */
function initSidebar() {
    const sidebar = document.getElementById('appSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (!sidebar || !overlay) return;
    
    // Cerrar sidebar al hacer clic en un enlace (solo en móvil)
    const navLinks = sidebar.querySelectorAll('.sidebar__nav-item');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 1024) {
                toggleSidebar();
            }
        });
    });
}

/**
 * Toggle sidebar (función global)
 */
function toggleSidebar() {
    const sidebar = document.getElementById('appSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('sidebar--open');
        overlay.classList.toggle('sidebar-overlay--active');
    }
}

/**
 * Inicializar alertas auto-dismiss
 */
function initAlerts() {
    const alerts = document.querySelectorAll('.alert--dismissible');
    
    alerts.forEach(alert => {
        // Auto-dismiss después de 5 segundos
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
}

/**
 * Inicializar tooltips (si se usan)
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const text = this.getAttribute('data-tooltip');
            showTooltip(this, text);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

/**
 * Mostrar tooltip
 */
function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.id = 'activeTooltip';
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
    tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
}

/**
 * Ocultar tooltip
 */
function hideTooltip() {
    const tooltip = document.getElementById('activeTooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Utilidad: Mostrar notificación
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('notification--show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('notification--show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Utilidad: Confirmar acción
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Utilidad: Formatear número como moneda
 */
function formatCurrency(amount, currency = 'MXN') {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Utilidad: Formatear fecha
 */
function formatDate(date, format = 'short') {
    const options = format === 'short' 
        ? { year: 'numeric', month: '2-digit', day: '2-digit' }
        : { year: 'numeric', month: 'long', day: 'numeric' };
    
    return new Intl.DateTimeFormat('es-MX', options).format(new Date(date));
}

// Exportar funciones globales
window.toggleSidebar = toggleSidebar;
window.showNotification = showNotification;
window.confirmAction = confirmAction;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
