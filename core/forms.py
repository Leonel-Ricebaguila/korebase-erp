from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Se enviará un código OTP.")
    first_name = forms.CharField(required=True, label="Nombre")
    last_name = forms.CharField(required=True, label="Apellidos")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
            'employee_id': 'ID único del empleado (ej. EMP-001).',
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        from .models import Company
        model = Company
        fields = ['name', 'rfc', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'erp-form-input', 'placeholder': 'Nombre Comercial / Razón Social'}),
            'rfc': forms.TextInput(attrs={'class': 'erp-form-input', 'placeholder': 'Ej. XAXX010101000'}),
            'logo': forms.FileInput(attrs={'class': 'erp-form-input', 'accept': 'image/*'}),
        }
        labels = {
            'name': 'Nombre de la Empresa',
            'rfc': 'RFC',
            'logo': 'Logotipo (Opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rfc'].required = False
        self.fields['logo'].required = False
