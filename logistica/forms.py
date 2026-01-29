"""
Forms for Logistics Module
KoreBase ERP System
"""
from django import forms
from .models import Product, Warehouse, Supplier


class ProductForm(forms.ModelForm):
    """Form for creating/editing products"""
    
    class Meta:
        model = Product
        fields = ['sku', 'name', 'description', 'category', 'unit_cost', 'active']
        widgets = {
            'sku': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: PROD-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Nombre del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'erp-form-textarea',
                'placeholder': 'Descripción detallada del producto',
                'rows': 4
            }),
            'category': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: Electrónicos'
            }),
            'unit_cost': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sku'].label = 'SKU'
        self.fields['name'].label = 'Nombre del Producto'
        self.fields['description'].label = 'Descripción'
        self.fields['category'].label = 'Categoría'
        self.fields['unit_cost'].label = 'Costo Unitario (MXN)'
        self.fields['active'].label = 'Activo'


class WarehouseForm(forms.ModelForm):
    """Form for creating/editing warehouses"""
    
    class Meta:
        model = Warehouse
        fields = ['code', 'name', 'address', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: ALM-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Nombre del almacén'
            }),
            'address': forms.Textarea(attrs={
                'class': 'erp-form-textarea',
                'placeholder': 'Dirección completa',
                'rows': 3
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = 'Código'
        self.fields['name'].label = 'Nombre del Almacén'
        self.fields['address'].label = 'Dirección'
        self.fields['active'].label = 'Activo'


class SupplierForm(forms.ModelForm):
    """Form for creating/editing suppliers"""
    
    class Meta:
        model = Supplier
        fields = ['code', 'name', 'contact_name', 'email', 'phone', 'address', 'active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: PROV-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Nombre de la empresa'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Nombre del contacto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'correo@ejemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '+52 999 123 4567'
            }),
            'address': forms.Textarea(attrs={
                'class': 'erp-form-textarea',
                'placeholder': 'Dirección completa',
                'rows': 3
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = 'Código'
        self.fields['name'].label = 'Nombre del Proveedor'
        self.fields['contact_name'].label = 'Nombre de Contacto'
        self.fields['email'].label = 'Email'
        self.fields['phone'].label = 'Teléfono'
        self.fields['address'].label = 'Dirección'
        self.fields['active'].label = 'Activo'
