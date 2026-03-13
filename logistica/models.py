"""
Logística Module - Supply Chain Management
KoreBase ERP System
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import TenantAwareModel


class Warehouse(TenantAwareModel):
    """Warehouse/Location model — Tenant-Isolated"""
    code = models.CharField(max_length=20, verbose_name="Código")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    address = models.TextField(verbose_name="Dirección", blank=True)
    active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"
        ordering = ['code']
        unique_together = [['company', 'code']]  # Unique per tenant, not globally

    def __str__(self):
        return f"{self.code} - {self.name}"


class Product(TenantAwareModel):
    """Product catalog — Tenant-Isolated"""
    sku = models.CharField(max_length=50, verbose_name="SKU")
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

    # Cumplimiento Fiscal MX (CFDI 4.0 - SAT)
    clave_producto_sat = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name="Clave Producto/Servicio SAT",
        help_text="Clave de 8 dígitos del catálogo del SAT (ej. 43211500)"
    )
    clave_unidad_sat = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name="Clave Unidad SAT",
        help_text="Clave de unidad del SAT (ej. H87 para piezas)"
    )

    active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['sku']
        unique_together = [['company', 'sku']]  # Unique per tenant, not globally

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Stock(TenantAwareModel):
    """Stock levels by warehouse — Tenant-Isolated"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name="Almacén")
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Cantidad"
    )

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = [['company', 'product', 'warehouse']]

    def __str__(self):
        return f"{self.product.sku} @ {self.warehouse.code}: {self.quantity}"


class StockMovement(TenantAwareModel):
    """Immutable stock movement log — Tenant-Isolated"""
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


class Supplier(TenantAwareModel):
    """Supplier/Vendor model — Tenant-Isolated"""
    code = models.CharField(max_length=20, verbose_name="Código")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    contact_name = models.CharField(max_length=200, verbose_name="Contacto", blank=True)
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['name']
        unique_together = [['company', 'code']]  # Unique per tenant, not globally

    def __str__(self):
        return f"{self.code} - {self.name}"

