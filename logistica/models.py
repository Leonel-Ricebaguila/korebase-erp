"""
Log ística Module - Supply Chain Management
KoreBase ERP System
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Warehouse(models.Model):
    """Warehouse/Location model"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    address = models.TextField(verbose_name="Dirección", blank=True)
    active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Product(models.Model):
    """Product catalog"""
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    category = models.CharField(max_length=100, verbose_name="Categoría")
    
    # Precio usando Decimal (NUNCA Float) - Regla de seguridad
    unit_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Costo Unitario"
    )
    
    active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['sku']
    
    def __str__(self):
        return f"{self.sku} - {self.name}"


class Stock(models.Model):
    """Stock levels by warehouse"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name="Almacén")
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Cantidad"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['product', 'warehouse']
        # Constraint removed for Django 6.0 compatibility - enforced via validator
    
    def __str__(self):
        return f"{self.product.sku} @ {self.warehouse.code}: {self.quantity}"


class StockMovement(models.Model):
    """Immutable stock movement log"""
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('adjustment', 'Ajuste'),
        ('transfer', 'Transferencia'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quantity_change = models.DecimalField(max_digits=15, decimal_places=3)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    reference = models.CharField(max_length=100, blank=True, verbose_name="Referencia")
    notes = models.TextField(blank=True, verbose_name="Notas")
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('core.CustomUser', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"
        ordering = ['-timestamp']
    
    def save(self, *args, **kwargs):
        # Registro inmutable - no permitir updates
        if self.pk is not None:
            raise ValueError("Stock movements are immutable after creation")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_movement_type_display()}: {self.product.sku} ({self.quantity_change})"


class Supplier(models.Model):
    """Supplier/Vendor model"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    contact_name = models.CharField(max_length=200, verbose_name="Contacto", blank=True)
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
