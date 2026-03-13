from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Q, DecimalField, Value, F
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from core.notifications import notify
import csv
from datetime import datetime
from decimal import Decimal

from .models import Product, Stock, Warehouse, Supplier, StockMovement
from .forms import ProductForm, WarehouseForm, SupplierForm, StockMovementForm


@login_required
def index(request):
    """Logística dashboard"""
    total_value_data = Stock.objects.aggregate(
        total=Sum(F('quantity') * F('product__unit_cost'), output_field=DecimalField())
    )
    total_value = total_value_data['total'] or Decimal('0.00')

    recent_movements = StockMovement.objects.select_related(
        'product', 'warehouse', 'user'
    ).order_by('-timestamp')[:5]

    context = {
        'total_products': Product.objects.filter(active=True).count(),
        'total_warehouses': Warehouse.objects.filter(active=True).count(),
        'total_suppliers': Supplier.objects.filter(active=True).count(),
        'total_value': total_value,
        'recent_products': Product.objects.filter(active=True).annotate(
            total_stock=Coalesce(Sum('stock__quantity'), Value(0), output_field=DecimalField())
        ).order_by('-created_at')[:5],
        'recent_movements': recent_movements,
    }
    return render(request, 'logistica/index.html', context)


@login_required
def inventory_list(request):
    """List all inventory with stock levels, filters, and search"""
    products = Product.objects.filter(active=True).annotate(
        total_stock=Coalesce(Sum('stock__quantity'), Value(0), output_field=DecimalField())
    )

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(sku__icontains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    category = request.GET.get('category')
    if category:
        products = products.filter(category__iexact=category)

    categories = Product.objects.filter(active=True).values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'search_query': query or '',
        'current_category': category or ''
    }
    return render(request, 'logistica/inventory_list.html', context)


@login_required
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.company = request.user.company  # Multi-Tenant assignment
            product.save()
            messages.success(request, f'Producto "{product.name}" creado exitosamente.')
            notify(request.user, f'Nuevo producto creado: {product.name}', 'success', f'/logistica/product/{product.pk}/edit/')
            return redirect('logistica:inventory_list')
    else:
        form = ProductForm()

    return render(request, 'logistica/product_form.html', {'form': form, 'title': 'Nuevo Producto'})


@login_required
def product_edit(request, pk):
    """Edit an existing product"""
    product = get_object_or_404(Product, pk=pk, company=request.user.company)  # Tenant-safe

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Producto "{product.name}" actualizado exitosamente.')
            notify(request.user, f'Producto modificado: {product.name}', 'info', f'/logistica/product/{product.pk}/edit/')
            return redirect('logistica:inventory_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'logistica/product_form.html', {'form': form, 'title': 'Editar Producto', 'product': product})


@login_required
def product_delete(request, pk):
    """Delete a product (soft delete by setting active=False)"""
    product = get_object_or_404(Product, pk=pk, company=request.user.company)  # Tenant-safe

    if request.method == 'POST':
        product.active = False
        product.save()
        messages.success(request, f'Producto "{product.name}" eliminado exitosamente.')
        notify(request.user, f'Producto eliminado: {product.name}', 'warning')
        return redirect('logistica:inventory_list')

    return render(request, 'logistica/product_confirm_delete.html', {
        'object': product,
        'title': 'Eliminar Producto',
        'cancel_url': 'logistica:inventory_list',
    })


@login_required
def product_history(request, pk):
    """View product movement history (Traceability)"""
    product = get_object_or_404(Product, pk=pk)
    movements = StockMovement.objects.filter(product=product).select_related('warehouse', 'user').order_by('-timestamp')

    stock_by_warehouse = Stock.objects.filter(product=product, quantity__gt=0).select_related('warehouse')

    context = {
        'product': product,
        'movements': movements,
        'stock_by_warehouse': stock_by_warehouse,
    }
    return render(request, 'logistica/product_history.html', context)


@login_required
@transaction.atomic
def stock_adjustment(request, pk):
    """Register stock movements (in/out/adjust) with audit trail"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = StockMovementForm(request.POST, company=request.user.company)
        if form.is_valid():
            warehouse = form.cleaned_data['warehouse']
            movement_type = form.cleaned_data['movement_type']
            quantity = form.cleaned_data['quantity']
            reference = form.cleaned_data['reference']
            notes = form.cleaned_data['notes']

            stock, created = Stock.objects.select_for_update().get_or_create(
                product=product,
                warehouse=warehouse,
                company=request.user.company,  # Multi-Tenant
                defaults={'quantity': Decimal('0.000')}
            )

            quantity_change = Decimal('0.000')

            if movement_type == 'in':
                stock.quantity += quantity
                quantity_change = quantity
            elif movement_type == 'out':
                if stock.quantity < quantity:
                    messages.error(request, f'Stock insuficiente en {warehouse.name}. Disponible: {stock.quantity}')
                    return render(request, 'logistica/stock_adjustment.html', {'form': form, 'product': product})
                stock.quantity -= quantity
                quantity_change = -quantity
            elif movement_type == 'adjustment':
                quantity_change = quantity - stock.quantity
                stock.quantity = quantity

            stock.save()

            StockMovement.objects.create(
                company=request.user.company,  # Multi-Tenant
                product=product,
                warehouse=warehouse,
                quantity_change=quantity_change,
                movement_type=movement_type,
                reference=reference,
                notes=notes,
                user=request.user
            )

            messages.success(request, 'Movimiento registrado exitosamente.')
            return redirect('logistica:product_history', pk=product.pk)
    else:
        form = StockMovementForm(company=request.user.company)

    # Show current stock by warehouse for this product
    stock_by_warehouse = Stock.objects.filter(product=product, quantity__gt=0).select_related('warehouse')

    return render(request, 'logistica/stock_adjustment.html', {
        'form': form,
        'product': product,
        'stock_by_warehouse': stock_by_warehouse,
    })


@login_required
def export_inventory_csv(request):
    """Export currently filtered inventory to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    writer.writerow(['SKU', 'Nombre', 'Categoría', 'Costo Unitario', 'Stock Total', 'Descripción'])

    products = Product.objects.filter(active=True).annotate(
        total_stock=Coalesce(Sum('stock__quantity'), Value(0), output_field=DecimalField())
    )

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(sku__icontains=query) |
            Q(name__icontains=query)
        )

    category = request.GET.get('category')
    if category:
        products = products.filter(category__iexact=category)

    for product in products:
        writer.writerow([
            product.sku,
            product.name,
            product.category,
            product.unit_cost,
            product.total_stock,
            product.description
        ])

    return response


# ------ Warehouses ------

@login_required
def warehouse_list(request):
    """List all warehouses"""
    warehouses = Warehouse.objects.all()

    query = request.GET.get('q')
    if query:
        warehouses = warehouses.filter(
            Q(code__icontains=query) | Q(name__icontains=query)
        )

    show_inactive = request.GET.get('inactive')
    if not show_inactive:
        warehouses = warehouses.filter(active=True)

    # Annotate with product count and total stock per warehouse
    warehouses = warehouses.annotate(
        product_count=Coalesce(
            Sum('stock__quantity', filter=Q(stock__quantity__gt=0), distinct=False),
            Value(0),
            output_field=DecimalField()
        )
    )

    context = {
        'warehouses': warehouses,
        'search_query': query or '',
        'show_inactive': show_inactive,
    }
    return render(request, 'logistica/warehouse_list.html', context)


@login_required
def warehouse_create(request):
    """Create a new warehouse"""
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.company = request.user.company  # Multi-Tenant assignment
            warehouse.save()
            messages.success(request, f'Almacén "{warehouse.name}" creado exitosamente.')
            notify(request.user, f'Nuevo almacén: {warehouse.name}', 'success')
            return redirect('logistica:warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'logistica/warehouse_form.html', {'form': form, 'title': 'Nuevo Almacén'})


@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, company=request.user.company)  # Tenant-safe
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, f'Almacén "{warehouse.name}" actualizado.')
            notify(request.user, f'Almacén modificado: {warehouse.name}', 'info', f'/logistica/warehouse/{warehouse.pk}/edit/')
            return redirect('logistica:warehouse_list')
    else:
        form = WarehouseForm(instance=warehouse)
    return render(request, 'logistica/warehouse_form.html', {'form': form, 'title': 'Editar Almacén', 'warehouse': warehouse})


@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, company=request.user.company)  # Tenant-safe
    if request.method == 'POST':
        warehouse.active = False
        warehouse.save()
        messages.success(request, f'Almacén "{warehouse.name}" eliminado.')
        notify(request.user, f'Almacén eliminado: {warehouse.name}', 'warning')
        return redirect('logistica:warehouse_list')

    return render(request, 'logistica/warehouse_confirm_delete.html', {
        'object': warehouse,
        'title': 'Eliminar Almacén',
        'cancel_url': 'logistica:warehouse_list',
    })


# ------ Suppliers ------

@login_required
def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.all()

    query = request.GET.get('q')
    if query:
        suppliers = suppliers.filter(
            Q(code__icontains=query) |
            Q(name__icontains=query) |
            Q(contact_name__icontains=query)
        )

    show_inactive = request.GET.get('inactive')
    if not show_inactive:
        suppliers = suppliers.filter(active=True)

    context = {
        'suppliers': suppliers,
        'search_query': query or '',
        'show_inactive': show_inactive,
    }
    return render(request, 'logistica/supplier_list.html', context)


@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.company = request.user.company  # Multi-Tenant assignment
            supplier.save()
            messages.success(request, f'Proveedor "{supplier.name}" creado.')
            notify(request.user, f'Nuevo proveedor: {supplier.name}', 'success')
            return redirect('logistica:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'logistica/supplier_form.html', {'form': form, 'title': 'Nuevo Proveedor'})


@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, company=request.user.company)  # Tenant-safe
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Proveedor "{supplier.name}" actualizado.')
            notify(request.user, f'Proveedor modificado: {supplier.name}', 'info', f'/logistica/supplier/{supplier.pk}/edit/')
            return redirect('logistica:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'logistica/supplier_form.html', {'form': form, 'title': 'Editar Proveedor', 'supplier': supplier})


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, company=request.user.company)  # Tenant-safe
    if request.method == 'POST':
        supplier.active = False
        supplier.save()
        messages.success(request, f'Proveedor "{supplier.name}" eliminado.')
        notify(request.user, f'Proveedor eliminado: {supplier.name}', 'warning')
        return redirect('logistica:supplier_list')

    return render(request, 'logistica/supplier_confirm_delete.html', {
        'object': supplier,
        'title': 'Eliminar Proveedor',
        'cancel_url': 'logistica:supplier_list',
    })
