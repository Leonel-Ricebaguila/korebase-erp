"""
Producción Module - MRP & Manufacturing
KoreBase ERP System
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class BillOfMaterial(models.Model):
    """Bill of Materials (BOM) - Lista de Materiales"""
    product = models.ForeignKey('logistica.Product', on_delete=models.PROTECT, verbose_name="Producto")
    version = models.IntegerField(default=1, verbose_name="Versión")
    active = models.BooleanField(default=True, verbose_name="Activo")
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('core.CustomUser', on_delete=models.PROTECT, related_name='boms_created')
    
    class Meta:
        verbose_name = "Lista de Materiales"
        verbose_name_plural = "Listas de Materiales"
        unique_together = ['product', 'version']
        ordering = ['product', '-version']
    
    def __str__(self):
        return f"BOM - {self.product.sku} v{self.version}"


class BOMLine(models.Model):
    """BOM Line Item - Component in BOM"""
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.CASCADE, related_name='lines')
    component = models.ForeignKey('logistica.Product', on_delete=models.PROTECT, verbose_name="Componente")
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Cantidad"
    )
    sequence = models.IntegerField(default=0, verbose_name="Secuencia")
    
    class Meta:
        verbose_name = "Línea de BOM"
        verbose_name_plural = "Líneas de BOM"
        ordering = ['bom', 'sequence']
    
    def __str__(self):
        return f"{self.component.sku} x {self.quantity}"


class WorkOrder(models.Model):
    """Work Order - Orden de Trabajo"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Proceso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    work_order_number = models.CharField(max_length=50, unique=True, verbose_name="Número de Orden")
    product = models.ForeignKey('logistica.Product', on_delete=models.PROTECT, verbose_name="Producto")
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.PROTECT, null=True, blank=True, verbose_name="BOM")
    
    quantity_planned = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Cantidad Planificada"
    )
    quantity_produced = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Cantidad Producida"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    warehouse = models.ForeignKey('logistica.Warehouse', on_delete=models.PROTECT, verbose_name=" Almacén")
    
    start_date = models.DateTimeField(verbose_name="Fecha Inicio")
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Finalización")
    
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('core.CustomUser', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Órdenes de Trabajo"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.work_order_number} - {self.product.sku}"
