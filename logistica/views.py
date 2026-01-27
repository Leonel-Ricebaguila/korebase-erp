from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product, Stock, Warehouse, Supplier


@login_required
def index(request):
    """Logística dashboard"""
    context = {
        'total_products': Product.objects.filter(active=True).count(),
        'total_warehouses': Warehouse.objects.filter(active=True).count(),
        'total_suppliers': Supplier.objects.filter(active=True).count(),
    }
    return render(request, 'logistica/index.html', context)


@login_required
def inventory_list(request):
    """List all inventory with stock levels"""
    products = Product.objects.filter(active=True).select_related()
    return render(request, 'logistica/inventory_list.html', {'products': products})
