"""
Forms for Producción Module
KoreBase ERP System
"""
from django import forms
from django.forms import inlineformset_factory
from .models import BillOfMaterial, BOMLine, WorkOrder


class BillOfMaterialForm(forms.ModelForm):
    """Form for creating/editing BOMs"""

    class Meta:
        model = BillOfMaterial
        fields = ['product', 'version', 'active', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'erp-form-input'}),
            'version': forms.NumberInput(attrs={'class': 'erp-form-input', 'min': '1'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'erp-form-textarea',
                'rows': 3,
                'placeholder': 'Notas sobre esta lista de materiales'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label = 'Producto Final'
        self.fields['version'].label = 'Versión'
        self.fields['active'].label = 'Activa'
        self.fields['notes'].label = 'Notas'


class BOMLineForm(forms.ModelForm):
    """Form for a single BOM line (component)"""

    class Meta:
        model = BOMLine
        fields = ['component', 'quantity', 'sequence']
        widgets = {
            'component': forms.Select(attrs={'class': 'erp-form-input'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.000',
                'step': '0.001',
                'min': '0.001',
            }),
            'sequence': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0',
                'min': '0',
            }),
        }


BOMLineFormSet = inlineformset_factory(
    BillOfMaterial,
    BOMLine,
    form=BOMLineForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class WorkOrderForm(forms.ModelForm):
    """Form for creating/editing work orders"""

    class Meta:
        model = WorkOrder
        fields = [
            'work_order_number', 'product', 'bom', 'quantity_planned',
            'warehouse', 'start_date', 'notes'
        ]
        widgets = {
            'work_order_number': forms.TextInput(attrs={
                'class': 'erp-form-input',
                'placeholder': 'Ej: OT-2026-001'
            }),
            'product': forms.Select(attrs={'class': 'erp-form-input'}),
            'bom': forms.Select(attrs={'class': 'erp-form-input'}),
            'quantity_planned': forms.NumberInput(attrs={
                'class': 'erp-form-input',
                'placeholder': '0.000',
                'step': '0.001',
                'min': '0.001',
            }),
            'warehouse': forms.Select(attrs={'class': 'erp-form-input'}),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'erp-form-input',
                'type': 'datetime-local'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'erp-form-textarea',
                'rows': 3,
                'placeholder': 'Notas sobre esta orden de trabajo'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_order_number'].label = 'Nº Orden de Trabajo'
        self.fields['product'].label = 'Producto'
        self.fields['bom'].label = 'Lista de Materiales (BOM)'
        self.fields['bom'].required = False
        self.fields['quantity_planned'].label = 'Cantidad Planificada'
        self.fields['warehouse'].label = 'Almacén'
        self.fields['start_date'].label = 'Fecha de Inicio'
        self.fields['notes'].label = 'Notas'
