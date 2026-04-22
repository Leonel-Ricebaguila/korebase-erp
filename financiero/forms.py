"""
Forms for Financiero Module
KoreBase ERP System
"""
from django import forms
from django.forms import inlineformset_factory
from .models import ChartOfAccounts, JournalEntry, JournalEntryLine, Invoice


class ChartOfAccountsForm(forms.ModelForm):
    """Form for creating/editing chart of accounts entries"""

    class Meta:
        model = ChartOfAccounts
        fields = ['account_code', 'account_name', 'account_type', 'parent', 'active']
        widgets = {
            'account_code': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: 1100'
            }),
            'account_name': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: Caja y Bancos'
            }),
            'account_type': forms.Select(attrs={
                'class': 'erp-form-input'
            }),
            'parent': forms.Select(attrs={
                'class': 'erp-form-input'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_code'].label = 'Código de Cuenta'
        self.fields['account_name'].label = 'Nombre de Cuenta'
        self.fields['account_type'].label = 'Tipo de Cuenta'
        self.fields['parent'].label = 'Cuenta Padre'
        self.fields['parent'].required = False
        self.fields['active'].label = 'Activa'


class JournalEntryForm(forms.ModelForm):
    """Form for journal entry header"""

    class Meta:
        model = JournalEntry
        fields = ['entry_number', 'entry_date', 'description']
        widgets = {
            'entry_number': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: AST-2026-001'
            }),
            'entry_date': forms.DateInput(attrs={
                'class': 'erp-form-input',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'erp-form-textarea',
                'placeholder': 'Descripción del asiento contable',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_number'].label = 'Número de Asiento'
        self.fields['entry_date'].label = 'Fecha'
        self.fields['description'].label = 'Descripción'


class JournalEntryLineForm(forms.ModelForm):
    """Form for a single journal entry line"""

    class Meta:
        model = JournalEntryLine
        fields = ['account', 'debit', 'credit', 'description']
        widgets = {
            'account': forms.Select(attrs={
                'class': 'erp-form-input'
            }),
            'debit': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'onfocus': 'this.select()'
            }),
            'credit': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'onfocus': 'this.select()'
            }),
            'description': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Descripción de línea'
            }),
        }


JournalEntryLineFormSet = inlineformset_factory(
    JournalEntry,
    JournalEntryLine,
    form=JournalEntryLineForm,
    extra=2,
    can_delete=True,
    min_num=2,
    validate_min=True,
)


class InvoiceForm(forms.ModelForm):
    """Form for creating/editing invoices"""

    class Meta:
        model = Invoice
        fields = [
            'invoice_number', 'invoice_type', 'customer_supplier',
            'invoice_date', 'due_date', 'subtotal', 'tax_amount', 'total'
        ]
        widgets = {
            'invoice_number': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: FAC-2026-001'
            }),
            'invoice_type': forms.Select(attrs={
                'class': 'erp-form-input'
            }),
            'customer_supplier': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Nombre del cliente o proveedor'
            }),
            'invoice_date': forms.DateInput(attrs={
                'class': 'erp-form-input',
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'erp-form-input',
                'type': 'date'
            }),
            'subtotal': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'onfocus': 'this.select()'
            }),
            'tax_amount': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'onfocus': 'this.select()'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'onfocus': 'this.select()'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_number'].label = 'Número de Factura'
        self.fields['invoice_type'].label = 'Tipo'
        self.fields['customer_supplier'].label = 'Cliente / Proveedor'
        self.fields['invoice_date'].label = 'Fecha de Factura'
        self.fields['due_date'].label = 'Fecha de Vencimiento'
        self.fields['subtotal'].label = 'Subtotal'
        self.fields['tax_amount'].label = 'IVA'
        self.fields['total'].label = 'Total'
