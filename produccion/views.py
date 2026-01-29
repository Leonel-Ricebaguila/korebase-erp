from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import WorkOrder, BillOfMaterial


@login_required
def index(request):
    """Producción dashboard"""
    context = {
        'total_work_orders': WorkOrder.objects.count(),
        'active_work_orders': WorkOrder.objects.filter(status='in_progress').count(),
        'total_boms': BillOfMaterial.objects.filter(active=True).count(),
    }
    return render(request, 'produccion/index.html', context)
