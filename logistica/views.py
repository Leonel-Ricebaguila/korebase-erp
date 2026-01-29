from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Product, Stock, Warehouse, Supplier
from .forms import ProductForm, WarehouseForm, SupplierForm


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


@login_required
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, f'Producto "{product.name}" creado exitosamente.')
            return redirect('logistica:index')
    else:
        form = ProductForm()
    
    return render(request, 'logistica/product_form.html', {'form': form, 'title': 'Nuevo Producto'})


@login_required
def product_edit(request, pk):
    """Edit an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Producto "{product.name}" actualizado exitosamente.')
            return redirect('logistica:inventory_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'logistica/product_form.html', {'form': form, 'title': 'Editar Producto', 'product': product})


@login_required
def product_delete(request, pk):
    """Delete a product (soft delete by setting active=False)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.active = False
        product.save()
        messages.success(request, f'Producto "{product.name}" eliminado exitosamente.')
        return redirect('logistica:inventory_list')
    
    return render(request, 'logistica/product_confirm_delete.html', {'product': product})


@login_required
def warehouse_create(request):
    """Create a new warehouse"""
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.save()
            messages.success(request, f'Almacén "{warehouse.name}" creado exitosamente.')
            return redirect('logistica:index')
    else:
        form = WarehouseForm()
    
    return render(request, 'logistica/warehouse_form.html', {'form': form, 'title': 'Nuevo Almacén'})


@login_required
def warehouse_edit(request, pk):
    """Edit an existing warehouse"""
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, f'Almacén "{warehouse.name}" actualizado exitosamente.')
            return redirect('logistica:index')
    else:
        form = WarehouseForm(instance=warehouse)
    
    return render(request, 'logistica/warehouse_form.html', {'form': form, 'title': 'Editar Almacén', 'warehouse': warehouse})


@login_required
def warehouse_delete(request, pk):
    """Delete a warehouse (soft delete by setting active=False)"""
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    if request.method == 'POST':
        warehouse.active = False
        warehouse.save()
        messages.success(request, f'Almacén "{warehouse.name}" eliminado exitosamente.')
        return redirect('logistica:index')
    
    return render(request, 'logistica/warehouse_confirm_delete.html', {'warehouse': warehouse})


@login_required
def supplier_create(request):
    """Create a new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            messages.success(request, f'Proveedor "{supplier.name}" creado exitosamente.')
            return redirect('logistica:index')
    else:
        form = SupplierForm()
    
    return render(request, 'logistica/supplier_form.html', {'form': form, 'title': 'Nuevo Proveedor'})


@login_required
def supplier_edit(request, pk):
    """Edit an existing supplier"""
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Proveedor "{supplier.name}" actualizado exitosamente.')
            return redirect('logistica:index')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'logistica/supplier_form.html', {'form': form, 'title': 'Editar Proveedor', 'supplier': supplier})


@login_required
def supplier_delete(request, pk):
    """Delete a supplier (soft delete by setting active=False)"""
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier.active = False
        supplier.save()
        messages.success(request, f'Proveedor "{supplier.name}" eliminado exitosamente.')
        return redirect('logistica:index')
    
    return render(request, 'logistica/supplier_confirm_delete.html', {'supplier': supplier})
