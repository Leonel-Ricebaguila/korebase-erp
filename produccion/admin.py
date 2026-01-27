from django.contrib import admin
from .models import BillOfMaterial, BOMLine, WorkOrder


class BOMLineInline(admin.TabularInline):
    model = BOMLine
    extra = 1


@admin.register(BillOfMaterial)
class BillOfMaterialAdmin(admin.ModelAdmin):
    list_display = ['product', 'version', 'active', 'created_at', 'created_by']
    list_filter = ['active', 'created_at']
    search_fields = ['product__sku', 'product__name']
    inlines = [BOMLineInline]
    readonly_fields = ['created_at', 'created_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['work_order_number', 'product', 'status', 'quantity_planned', 'quantity_produced', 'start_date']
    list_filter = ['status', 'start_date']
    search_fields = ['work_order_number', 'product__sku']
    readonly_fields = ['created_at', 'created_by']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
