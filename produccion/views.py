"""
Producción Views - Manufacturing & MRP CRUD
KoreBase ERP System
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count

from .models import BillOfMaterial, BOMLine, WorkOrder
from .forms import BillOfMaterialForm, BOMLineFormSet, WorkOrderForm


# ==================== DASHBOARD ====================

@login_required
def index(request):
    """Producción dashboard with real KPIs"""
    total_boms = BillOfMaterial.objects.filter(active=True).count()
    total_work_orders = WorkOrder.objects.count()
    active_work_orders = WorkOrder.objects.filter(status__in=['pending', 'in_progress']).count()
    completed_work_orders = WorkOrder.objects.filter(status='completed').count()

    # Status breakdown for cards
    pending_orders = WorkOrder.objects.filter(status='pending').count()
    in_progress_orders = WorkOrder.objects.filter(status='in_progress').count()

    # Recent work orders
    recent_orders = WorkOrder.objects.select_related('product', 'warehouse').order_by('-created_at')[:5]

    context = {
        'total_boms': total_boms,
        'total_work_orders': total_work_orders,
        'active_work_orders': active_work_orders,
        'completed_work_orders': completed_work_orders,
        'pending_orders': pending_orders,
        'in_progress_orders': in_progress_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'produccion/index.html', context)


# ==================== BILL OF MATERIALS ====================

@login_required
def bom_list(request):
    """List all BOMs"""
    boms = BillOfMaterial.objects.select_related('product', 'created_by') \
        .annotate(component_count=Count('lines')) \
        .order_by('product__sku', '-version')

    query = request.GET.get('q')
    if query:
        boms = boms.filter(
            Q(product__sku__icontains=query) |
            Q(product__name__icontains=query) |
            Q(notes__icontains=query)
        )

    show_inactive = request.GET.get('inactive') == '1'
    if not show_inactive:
        boms = boms.filter(active=True)

    context = {
        'boms': boms,
        'search_query': query or '',
        'show_inactive': show_inactive,
    }
    return render(request, 'produccion/bom_list.html', context)


@login_required
@transaction.atomic
def bom_create(request):
    """Create a new BOM with component lines"""
    company = request.user.company
    if request.method == 'POST':
        form = BillOfMaterialForm(request.POST, company=company)
        if form.is_valid():
            bom = form.save(commit=False)
            bom.created_by = request.user
            bom.company = company  # Multi-Tenant
            bom.save()

            formset = BOMLineFormSet(request.POST, instance=bom)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'BOM "{bom}" creada exitosamente.')
                return redirect('produccion:bom_detail', pk=bom.pk)
            else:
                bom.delete()
                messages.error(request, 'Corrige los errores en los componentes.')
        else:
            formset = BOMLineFormSet(request.POST)
    else:
        form = BillOfMaterialForm(company=company)
        formset = BOMLineFormSet()

    return render(request, 'produccion/bom_form.html', {
        'form': form, 'formset': formset, 'title': 'Nueva Lista de Materiales'
    })


@login_required
@transaction.atomic
def bom_edit(request, pk):
    """Edit an existing BOM"""
    company = request.user.company
    bom = get_object_or_404(BillOfMaterial, pk=pk, company=company)  # Tenant-safe

    if request.method == 'POST':
        form = BillOfMaterialForm(request.POST, instance=bom, company=company)
        formset = BOMLineFormSet(request.POST, instance=bom)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'BOM "{bom}" actualizada.')
            return redirect('produccion:bom_detail', pk=bom.pk)
        else:
            messages.error(request, 'Corrige los errores.')
    else:
        form = BillOfMaterialForm(instance=bom, company=company)
        formset = BOMLineFormSet(instance=bom)

    return render(request, 'produccion/bom_form.html', {
        'form': form, 'formset': formset, 'title': 'Editar BOM', 'bom': bom
    })


@login_required
def bom_detail(request, pk):
    """View a BOM with all component lines"""
    bom = get_object_or_404(BillOfMaterial, pk=pk)
    lines = bom.lines.select_related('component').order_by('sequence')

    context = {
        'bom': bom,
        'lines': lines,
    }
    return render(request, 'produccion/bom_detail.html', context)


# ==================== WORK ORDERS ====================

@login_required
def workorder_list(request):
    """List all work orders"""
    orders = WorkOrder.objects.select_related('product', 'warehouse', 'bom').order_by('-start_date')

    query = request.GET.get('q')
    if query:
        orders = orders.filter(
            Q(work_order_number__icontains=query) |
            Q(product__sku__icontains=query) |
            Q(product__name__icontains=query)
        )

    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'status_choices': WorkOrder.STATUS_CHOICES,
        'current_status': status_filter or '',
        'search_query': query or '',
    }
    return render(request, 'produccion/workorder_list.html', context)


@login_required
def workorder_create(request):
    """Create a new work order"""
    company = request.user.company
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, company=company)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.company = company  # Multi-Tenant
            order.save()
            messages.success(request, f'Orden "{order.work_order_number}" creada exitosamente.')
            return redirect('produccion:workorder_detail', pk=order.pk)
    else:
        form = WorkOrderForm(company=company)

    return render(request, 'produccion/workorder_form.html', {
        'form': form, 'title': 'Nueva Orden de Trabajo'
    })


@login_required
def workorder_edit(request, pk):
    """Edit a work order (only if pending)"""
    company = request.user.company
    order = get_object_or_404(WorkOrder, pk=pk, company=company)  # Tenant-safe

    if order.status not in ['pending']:
        messages.error(request, 'Solo se pueden editar órdenes en estado Pendiente.')
        return redirect('produccion:workorder_detail', pk=pk)

    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=order, company=company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Orden "{order.work_order_number}" actualizada.')
            return redirect('produccion:workorder_detail', pk=order.pk)
    else:
        form = WorkOrderForm(instance=order, company=company)

    return render(request, 'produccion/workorder_form.html', {
        'form': form, 'title': 'Editar Orden de Trabajo', 'order': order
    })


@login_required
def workorder_detail(request, pk):
    """View a work order detail"""
    order = get_object_or_404(WorkOrder.objects.select_related('product', 'warehouse', 'bom', 'created_by'), pk=pk)

    bom_lines = []
    if order.bom:
        bom_lines = order.bom.lines.select_related('component').order_by('sequence')

    context = {
        'order': order,
        'bom_lines': bom_lines,
    }
    return render(request, 'produccion/workorder_detail.html', context)


@login_required
def workorder_status(request, pk):
    """Change work order status with valid transitions"""
    order = get_object_or_404(WorkOrder, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        valid_transitions = {
            'pending': ['in_progress', 'cancelled'],
            'in_progress': ['completed', 'cancelled'],
            'completed': [],
            'cancelled': [],
        }

        allowed = valid_transitions.get(order.status, [])
        if new_status not in allowed:
            messages.error(
                request,
                f'No se puede cambiar de "{order.get_status_display()}" a "{new_status}".'
            )
            return redirect('produccion:workorder_detail', pk=pk)

        # If completing, update quantity_produced
        if new_status == 'completed':
            from django.utils import timezone
            order.quantity_produced = order.quantity_planned
            order.completion_date = timezone.now()

        order.status = new_status
        order.save()

        status_labels = dict(WorkOrder.STATUS_CHOICES)
        messages.success(
            request,
            f'Orden "{order.work_order_number}" ahora está: {status_labels.get(new_status, new_status)}.'
        )

    return redirect('produccion:workorder_detail', pk=pk)
