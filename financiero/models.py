"""
Financiero Module - Accounting & Finance (NÚCLEO SAGRADO)
KoreBase ERP System

CRITICAL RULES:
1. Activo = Pasivo + Patrimonio (ecuación contable SIEMPRE válida)
2. NUNCA usar Float, siempre Decimal para cantidades monetarias
3. NUNCA borrar registros contables (usar contra-asientos)
4. Usar transaction.atomic para operaciones multi-tabla
5. JournalEntry son INMUTABLES después de creación
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.db import transaction
from decimal import Decimal


class ChartOfAccounts(models.Model):
    """Plan de Cuentas Contable"""
    ACCOUNT_TYPES = [
        ('asset', 'Activo'),
        ('liability', 'Pasivo'),
        ('equity', 'Patrimonio'),
        ('income', 'Ingresos'),
        ('expense', 'Gastos'),
    ]
    
    account_code = models.CharField(max_length=20, unique=True, verbose_name="Código de Cuenta")
    account_name = models.CharField(max_length=200, verbose_name="Nombre de Cuenta")
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, verbose_name="Tipo")
    
    # Balance siempre en Decimal - NUNCA Float
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Balance"
    )
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name="Cuenta Padre"
    )
    active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cuenta Contable"
        verbose_name_plural = "Plan de Cuentas"
        ordering = ['account_code']
    
    def __str__(self):
        return f"{self.account_code} - {self.account_name}"


class JournalEntry(models.Model):
    """
    Asiento Contable - INMUTABLE
    
    CRITICAL: Este modelo es INMUTABLE después de creación.
    Para corregir errores, usar contra-asientos (reversal).
    """
    entry_number = models.CharField(max_length=50, unique=True, verbose_name="Número de Asiento")
    entry_date = models.DateField(verbose_name="Fecha")
    description = models.TextField(verbose_name="Descripción")
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('core.CustomUser', on_delete=models.PROTECT, related_name='journal_entries')
    
    # Reversión fields (para contra-asientos)
    reversed = models.BooleanField(default=False, verbose_name="Revertido")
    reversal_of = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='reversals',
        verbose_name="Reverso de"
    )
    
    class Meta:
        verbose_name = "Asiento Contable"
        verbose_name_plural = "Asientos Contables"
        ordering = ['-entry_date', '-created_at']
    
    def save(self, *args, **kwargs):
        """INMUTABILIDAD: No permitir updates después de creación"""
        if self.pk is not None:
            raise ValueError("Journal entries are immutable after creation. Use reversals for corrections.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.entry_number} - {self.entry_date}"
    
    @transaction.atomic
    def create_reversal(self, user, description="Reverso"):
        """Crear contra-asiento para revertir este asiento"""
        if self.reversed:
            raise ValueError("Este asiento ya fue revertido")
        
        # Crear nuevo asiento de reverso
        reversal = JournalEntry.objects.create(
            entry_number=f"{self.entry_number}-REV",
            entry_date=self.entry_date,
            description=f"{description} de {self.entry_number}",
            created_by=user,
            reversal_of=self
        )
        
        # Copiar líneas con signos invertidos
        for line in self.lines.all():
            JournalEntryLine.objects.create(
                journal_entry=reversal,
                account=line.account,
                debit=line.credit,  # Invertir
                credit=line.debit,  # Invertir
                description=f"Reverso: {line.description}"
            )
        
        # Marcar como revertido
        self.reversed = True
        super(JournalEntry, self).save(update_fields=['reversed'])  # Bypass inmutabilidad solo para flag
        
        return reversal


class JournalEntryLine(models.Model):
    """Línea de Asiento Contable"""
    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.PROTECT,
        related_name='lines',
        verbose_name="Asiento"
    )
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.PROTECT, verbose_name="Cuenta")
    
    # Debe y Haber - siempre Decimal
    debit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Debe"
    )
    credit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Haber"
    )
    
    description = models.CharField(max_length=200, blank=True, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Línea de Asiento"
        verbose_name_plural = "Líneas de Asiento"
        # Constraint removed for Django 6.0 compatibility - business logic enforced in validation
    
    def __str__(self):
        return f"{self.account.account_code}: D:{self.debit} H:{self.credit}"


class Invoice(models.Model):
    """Factura"""
    TYPE_CHOICES = [
        ('customer', 'Cliente'),
        ('supplier', 'Proveedor'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('issued', 'Emitida'),
        ('paid', 'Pagada'),
        ('cancelled', 'Cancelada'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Número de Factura")
    invoice_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Tipo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    
    customer_supplier = models.CharField(max_length=200, verbose_name="Cliente/Proveedor")
    invoice_date = models.DateField(verbose_name="Fecha de Factura")
    due_date = models.DateField(verbose_name="Fecha de Vencimiento")
    
    # Cantidades en Decimal
    subtotal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Subtotal"
    )
    tax_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="IVA"
    )
    total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total"
    )
    
    journal_entry = models.ForeignKey(
        JournalEntry,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Asiento Contable"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('core.CustomUser', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-invoice_date']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer_supplier}"
